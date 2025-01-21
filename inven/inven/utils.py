from django.urls import reverse
import qrcode
from io import BytesIO
import base64

def dynamic_url(request, view_name, *args, **kwargs):
    path = reverse(view_name, args=args, kwargs=kwargs)
    domain = request.get_host()  # Gets the current host (e.g., localhost:8000)
    scheme = 'https' if request.is_secure() else 'http'  # Determines http/https
    return f"{scheme}://{domain}{path}"


def generate_qrcode(data: str, size: int = 256) -> str:

    img = qrcode.make(data)
    img = img.resize((size, size))
    
    # Convert image to base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    qr_code_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    
    return qr_code_base64