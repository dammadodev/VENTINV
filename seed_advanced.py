import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser
from apps.inventory.models import Category, Product, StockMovement
from apps.suppliers.models import Supplier
from apps.customers.models import Customer
from apps.cash.models import CashSession

def seed():
    print("Iniciando sembrado de datos avanzados...")

    # 1. Usuarios con roles
    roles_config = [
        ('admin', 'admin123', CustomUser.Role.ADMIN, 'Admin', 'Principal', True),
        ('empleado', 'empleado123', CustomUser.Role.EMPLEADO, 'Empleado', 'Vendedor', False),
        ('cajero', 'cajero123', CustomUser.Role.CAJERO, 'Carlos', 'Cajero', False),
        ('bodega', 'bodega123', CustomUser.Role.INVENTARIO, 'Ignacio', 'Inventario', False),
        ('auditor', 'auditor123', CustomUser.Role.AUDITOR, 'Ana', 'Auditora', False),
    ]

    for uname, pwd, rchoice, fname, lname, is_sup in roles_config:
        u, created = CustomUser.objects.get_or_create(
            username=uname,
            defaults={
                'email': f'{uname}@ventinv.com',
                'first_name': fname,
                'last_name': lname,
                'role': rchoice,
                'is_staff': is_sup,
                'is_superuser': is_sup,
            }
        )
        if created:
            u.set_password(pwd)
            u.save()
            print(f"[OK] Usuario {uname} ({rchoice}) creado. Password: {pwd}")

    # 2. Proveedores
    prov_1, _ = Supplier.objects.get_or_create(
        document_id='900123456-1',
        defaults={'name': 'Distribuidora Nacional S.A.S.', 'phone': '3101234567', 'contact_person': 'Mario Gómez'}
    )
    prov_2, _ = Supplier.objects.get_or_create(
        document_id='800987654-2',
        defaults={'name': 'Comercializadora del Sur Ltda.', 'phone': '3209876543', 'contact_person': 'Luisa Martínez'}
    )
    print("[OK] Proveedores de prueba listos.")

    # 3. Clientes
    cli_1, _ = Customer.objects.get_or_create(
        document_id='1098765432',
        defaults={'name': 'Empresa Soluciones T.I.', 'phone': '3157778899', 'credit_limit': 500000, 'current_balance': 0}
    )
    cli_2, _ = Customer.objects.get_or_create(
        document_id='98765432',
        defaults={'name': 'María Fernanda Rojas', 'phone': '3001112233', 'credit_limit': 200000, 'current_balance': 45000}
    )
    print("[OK] Clientes de prueba listos.")

    # 4. Aperturar Caja de Prueba
    admin_u = CustomUser.objects.get(username='admin')
    open_cash = CashSession.objects.filter(status=CashSession.Status.OPEN).first()
    if not open_cash:
        CashSession.objects.create(
            opened_by=admin_u,
            initial_amount=100000,
            status=CashSession.Status.OPEN
        )
        print("[OK] Caja registradora aperturada con $100,000 de fondo inicial.")

    print("\nSembrado de datos avanzados finalizado con exito!")

if __name__ == '__main__':
    seed()
