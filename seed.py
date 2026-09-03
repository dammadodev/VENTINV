import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import CustomUser
from apps.inventory.models import Category, Product, StockMovement

def seed_data():
    print("Iniciando sembrado de datos iniciales...")

    # 1. Crear Administrador
    admin_user, created_admin = CustomUser.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@ventinv.com',
            'first_name': 'Administrador',
            'last_name': 'Principal',
            'role': CustomUser.Role.ADMIN,
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created_admin:
        admin_user.set_password('admin123')
        admin_user.save()
        print("[OK] Usuario Admin creado: username='admin', password='admin123'")
    else:
        print("[OK] Usuario Admin ya existia.")

    # 2. Crear Empleado
    emp_user, created_emp = CustomUser.objects.get_or_create(
        username='empleado',
        defaults={
            'email': 'empleado@ventinv.com',
            'first_name': 'Juan',
            'last_name': 'Perez',
            'role': CustomUser.Role.EMPLEADO,
            'is_staff': False,
            'is_superuser': False,
        }
    )
    if created_emp:
        emp_user.set_password('empleado123')
        emp_user.save()
        print("[OK] Usuario Empleado creado: username='empleado', password='empleado123'")
    else:
        print("[OK] Usuario Empleado ya existia.")

    # 3. Categorias de ejemplo
    cat_bebidas, _ = Category.objects.get_or_create(name='Bebidas', defaults={'description': 'Gaseosas, jugos y agua.'})
    cat_snacks, _ = Category.objects.get_or_create(name='Snacks', defaults={'description': 'Papas, galletas y golosinas.'})
    cat_abarrotes, _ = Category.objects.get_or_create(name='Abarrotes', defaults={'description': 'Productos de primera necesidad.'})

    # 4. Productos de ejemplo
    products_data = [
        {'sku': 'BEB-001', 'name': 'Agua Mineral 600ml', 'category': cat_bebidas, 'cost_price': 1000, 'sale_price': 2000, 'stock': 50, 'min_stock': 10},
        {'sku': 'BEB-002', 'name': 'Gaseosa Cola 1.5L', 'category': cat_bebidas, 'cost_price': 3500, 'sale_price': 5000, 'stock': 25, 'min_stock': 5},
        {'sku': 'SNK-001', 'name': 'Papas Fritas Crujientes 110g', 'category': cat_snacks, 'cost_price': 2000, 'sale_price': 3500, 'stock': 40, 'min_stock': 8},
        {'sku': 'SNK-002', 'name': 'Chocolate con Mani 50g', 'category': cat_snacks, 'cost_price': 1200, 'sale_price': 2500, 'stock': 4, 'min_stock': 10}, # Alerta stock bajo
        {'sku': 'ABA-001', 'name': 'Arroz Premium 1kg', 'category': cat_abarrotes, 'cost_price': 3000, 'sale_price': 4500, 'stock': 60, 'min_stock': 15},
    ]

    for p_data in products_data:
        p, created = Product.objects.get_or_create(
            sku=p_data['sku'],
            defaults=p_data
        )
        if created:
            StockMovement.objects.create(
                product=p,
                movement_type=StockMovement.MovementType.ENTRY,
                quantity=p.stock,
                notes="Carga inicial de prueba",
                created_by=admin_user
            )
            print(f"[OK] Producto creado: {p.name} (Stock: {p.stock})")

    print("\nSembrado completado con exito!")

if __name__ == '__main__':
    seed_data()
