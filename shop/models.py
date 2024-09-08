from django.db import models
from django.core.files.storage import default_storage
from datetime import datetime,date
from jinja2 import Template
from weasyprint import HTML
import json
import os



# Create your models here.

class Product(models.Model):
    productId = models.AutoField
    productName = models.CharField(max_length = 50,default = "")
    category = models.CharField(max_length = 50,default = "")
    sub_category = models.CharField(max_length = 50,default = "")
    price = models.IntegerField(default = 0)
    desc = models.CharField(max_length = 300)
    pubDate = models.DateField()
    image = models.ImageField(upload_to = "shop/images", default = "")

    def __str__ (self):
        return self.productName
    
class Contact(models.Model):
    msgId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=50,default = '')
    userEmail = models.CharField(max_length=50,default='')
    userPhone = models.CharField(max_length=15,default='')
    userMessage = models.CharField(max_length=500,default='')
    messageDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userName
    
class Order(models.Model):
    ordId = models.AutoField(primary_key = True)
    cart = models.CharField(max_length = 2000)
    name = models.CharField(max_length = 30)
    email = models.CharField(max_length = 30)
    phone = models.CharField(max_length = 15,default='')
    address = models.CharField(max_length = 300)
    city = models.CharField(max_length = 30)
    state = models.CharField(max_length = 30)
    zipCode = models.CharField(max_length = 10)

    def __str__(self):
        return self.name
    
class OrderUpdate(models.Model):
    updateId = models.AutoField(primary_key = True)
    ordId = models.IntegerField()
    updates = models.JSONField(default = list,blank = True)

    def __str__ (self):
        return 'Order No : '+str(self.ordId)
    
    def setUpdate(self,newUpdateText):
        try:
            newUp = {
                'updateText':newUpdateText,
                'updateTime':datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            }
            self.updates.insert(0,newUp)
            self.save()
            return True
        except Exception as e:
            print(f"Exception Occured:{e}")
            return False

class Invoice(models.Model):
    invoiceId = models.AutoField(primary_key=True)
    ordId = models.IntegerField()
    pdf = models.FileField(upload_to = 'shop/invoice',null = True,blank = True)

    def __str__(self):
        return f'Invoice {self.invoiceId} for Order {self.ordId}'
    
    def generateSum(self, order):
        items_summary = []
        
        # Parse the JSON string in order.cart to a dictionary
        try:
            # Assuming order.cart is a JSON string like '{"product_id": [quantity,'name']}'
            cart = json.loads(order.cart)  
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in order.cart for order ID {order.ordId}")
        
        # Iterate over cart items
        for key, value in cart.items():
            try:
                # Fetch the product using the key (pr{id})
                product = Product.objects.get(id=int(key[-1]))
                
                # Calculate the total price for the product (unit price * quantity)
                quantity = value[0]  
                total_price = product.price * quantity
                
                # Append the item details: [Product Name, Unit Price, Quantity, Total Price]
                items_summary.append([product.productName, product.price, quantity, total_price])
            
            except Product.DoesNotExist:
                raise ValueError(f"Product with ID {key} does not exist.")
        
        return items_summary

    def generateInvoicePdf(self):

        try:
            # Fetch the order
            order = Order.objects.get(ordId=self.ordId)
            
            # Generate the items list by parsing order.cart (JSON field)
            items = self.generateSum(order)
            
            # Calculate the subtotal (sum of item totals)
            subtotal = sum(item[3] for item in items)
            
            # Adding 10% tax
            tax_rate = 0.10
            tax_amount = subtotal * tax_rate
            total = subtotal + tax_amount
            
            # Invoice data for the template
            invoice_data = {
                'company_name': 'Manorji Ki Duakn Pvt. Ltd.',
                'company_address': '123 App Street, Tech City',
                'company_contact': 'contact@manorjikiduakn.com',
                'client_name': order.name,
                'client_email': order.email,
                'client_phone': order.phone,
                'client_address': f"{order.address}, {order.city} ({order.zipCode}), {order.state}",
                'invoice_number': f'INV-{date.today().year}-{self.invoiceId}',  # Ensure self.invoiceId is set
                'invoice_date': date.today().strftime('%B %d, %Y'),
                'items': items,
                'subtotal': subtotal,
                'tax_amount': tax_amount,
                'total_amount': total
            }
            
            # HTML Invoice Template
            invoice_template = """
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body { font-family: 'Arial', sans-serif; }
                        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                        td, th { border: 1px solid #ddd; padding: 8px; text-align: left; }
                        th { background-color: #f2f2f2; }
                        h2, h3, h4 { margin-bottom: 5px; }
                    </style>
                </head>
                <body>
                    <h2>{{ company_name }}</h2>
                    <p>{{ company_address }}</p>
                    <p>{{ company_contact }}</p>
                    <hr>
                    <h3>Invoice: {{ invoice_number }}</h3>
                    <p>Date: {{ invoice_date }}</p>
                    <h4>Bill To:</h4>
                    <p>{{ client_name }}</p>
                    <p>{{ client_address }}</p>
                    <p>{{ client_phone }}</p>
                    <p>{{ client_email }}</p>
                    <hr>
                    <table>
                        <tr>
                            <th>Product</th>
                            <th>Quantity</th>
                            <th>Unit Price</th>
                            <th>Total</th>
                        </tr>
                        {% for item in items %}
                        <tr>
                            <td>{{ item.0 }}</td>
                            <td>{{ item.2 }}</td>
                            <td>{{ item.1 }}</td>
                            <td>{{ item.3 }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                    <hr>
                    <p>Subtotal: {{ subtotal }}</p>
                    <p>Tax (10.0%): {{ tax_amount }}</p>
                    <h3>Total: {{ total_amount }}</h3>
                </body>
                </html>
            """
            
            # Create a Django template and render it with the invoice data
            template = Template(invoice_template)
            rendered_html = template.render(invoice_data)

            # Generate PDF
            pdf_content = HTML(string=rendered_html).write_pdf()

            # Save the PDF
            pdf_file_path = f'shop/invoice/invoice_{self.invoiceId}.pdf'
            with default_storage.open(pdf_file_path, 'wb') as f:
                f.write(pdf_content)

            # Save the file to the FileField
            self.pdf.name = pdf_file_path
            self.save()


        except Order.DoesNotExist:
            raise ValueError(f"Order with ordId {self.ordId} not found")

        except Product.DoesNotExist as e:
            raise ValueError(f"Product not found: {str(e)}")

        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in order.cart for order ID {self.ordId}")

        except Exception as e:
            raise ValueError(f"Error generating invoice PDF: {str(e)}")