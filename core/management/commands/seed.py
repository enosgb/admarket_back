import random
from decimal import Decimal
import requests
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from ads.models import Category, Product  # Ajuste se o app for diferente

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Popula o banco com categoria, 1000 produtos e dois usuários (admin e normal)"
    )

    def handle(self, *args, **options):
        self.stdout.write("Iniciando o seed do banco de dados...\n")

        # === Download das imagens ===
        self.stdout.write("Baixando imagens das camisas dos times...")
        list_urls = [
            "https://i.ibb.co/Myg11shZ/America-MG.jpg",
            "https://i.ibb.co/84SXpY9C/Athletico-PR.png",
            "https://i.ibb.co/bMVvJ6dG/Atletico-GO.jpg",
            "https://i.ibb.co/S9YHTpV/Atletico-MG.jpg",
            "https://i.ibb.co/cSQRcvxV/Avai.jpg",
            "https://i.ibb.co/B2QMPFG5/Bahia.webp",
            "https://i.ibb.co/fVF94tkr/Botafogo.jpg",
            "https://i.ibb.co/pvHDZDtF/Ceara.png",
            "https://i.ibb.co/7tSBY1Ld/Chapecoense.png",
            "https://i.ibb.co/KcKwjg3t/Corinthians.png",
            "https://i.ibb.co/fdBT6F4r/Coritiba.png",
            "https://i.ibb.co/wNjjcgWX/CRB.jpg",
            "https://i.ibb.co/0RyprpPH/Cruzeiro.jpg",
            "https://i.ibb.co/twVrWf5p/CSA.jpg",
            "https://i.ibb.co/MxFy71GB/Figueirense.png",
            "https://i.ibb.co/bjQsphm6/Flamengo.jpg",
            "https://i.ibb.co/wrdyDgwm/Fluminense.png",
            "https://i.ibb.co/TMq1V0J7/Fortaleza.jpg",
            "https://i.ibb.co/PZwF3YXp/Goias.jpg",
            "https://i.ibb.co/S7vMCYtp/Gremio.jpg",
            "https://i.ibb.co/xK2svfLG/Guarani.jpg",
            "https://i.ibb.co/LdsxJnpQ/Internacional.webp",
            "https://i.ibb.co/LX6mP74M/Nautico.png",
            "https://i.ibb.co/nN4mNqJq/Palmeiras.jpg",
            "https://i.ibb.co/CK8gvx6b/Parana-Clube.jpg",
            "https://i.ibb.co/zWsc4fyS/Paysandu.jpg",
            "https://i.ibb.co/cSsbPbHT/Ponte-Preta.jpg",
            "https://i.ibb.co/9Hs1VgG5/Remo.jpg",
            "https://i.ibb.co/h3NsGf6/Santa-Cruz.jpg",
            "https://i.ibb.co/wNgw0PBG/Santos.png",
            "https://i.ibb.co/99RMny4g/Sao-Paulo.jpg",
            "https://i.ibb.co/gLCKSrkv/Sport-Recife.jpg",
            "https://i.ibb.co/Wv0PvQ3k/Vasco.png",
            "https://i.ibb.co/bjyvJhmW/Vila-Nova.jpg",
            "https://i.ibb.co/kgdBDws1/Vitoria.jpg",
        ]

        teams = [
            url.split("/")[-1]
            .replace(".jpg", "")
            .replace(".png", "")
            .replace(".webp", "")
            .replace("-", " ")
            for url in list_urls
        ]

        images_content = {}
        success_count = 0
        for url in list_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    images_content[url] = response.content
                    success_count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Falha ao baixar {url}: {e}"))
        self.stdout.write(
            self.style.SUCCESS(
                f"{success_count}/{len(list_urls)} imagens baixadas com sucesso.\n"
            )
        )

        # === Categoria ===
        self.stdout.write("Criando/verificando categoria...")
        category, created = Category.objects.get_or_create(
            name="Camisas de Times Brasileiros",
            defaults={
                "description": "Camisas oficiais de times de futebol brasileiros, incluindo uniformes home, away e third.",
                "active": True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Categoria criada!"))
        else:
            self.stdout.write(self.style.NOTICE("Categoria já existia, reutilizando."))

        # Adiciona imagem na categoria (se ainda não tiver)
        if not category.image and images_content:
            first_url = list_urls[0]
            content = images_content.get(first_url)
            if content:
                ext = first_url.split(".")[-1]
                category.image.save(f"category_camisas.{ext}", ContentFile(content))
                category.save()
                self.stdout.write(self.style.SUCCESS("Imagem adicionada à categoria."))

        # === Usuários ===
        self.stdout.write("\nCriando usuários...")

        admin_user, admin_created = User.objects.get_or_create(
            email="admin@exemplo.com",
            defaults={"name": "Administrador", "is_staff": True, "is_superuser": True},
        )
        if admin_created:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "Usuário admin criado: admin@exemplo.com (senha: admin123)"
                )
            )
        else:
            self.stdout.write(self.style.NOTICE("Usuário admin já existia."))

        normal_user, normal_created = User.objects.get_or_create(
            email="usuario@exemplo.com",
            defaults={
                "name": "Usuário Normal",
                "is_staff": False,
                "is_superuser": False,
            },
        )
        if normal_created:
            normal_user.set_password("user123")
            normal_user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "Usuário normal criado: usuario@exemplo.com (senha: user123)"
                )
            )
        else:
            self.stdout.write(self.style.NOTICE("Usuário normal já existia."))

        # === Produtos ===
        self.stdout.write(
            "\nCriando 1000 produtos... (isso pode levar alguns segundos)"
        )
        kits = ["Home", "Away", "Third"]
        sizes = ["P", "M", "G", "GG", "GGG"]
        num_products = 1000
        created_count = 0

        for i in range(num_products):
            idx = i % len(list_urls)
            url = list_urls[idx]
            team = teams[idx]

            name = f"Camisa {team} {random.choice(kits)} 2025"
            description = f"Camisa oficial do {team}, edição {random.choice(kits).lower()}. Material de alta qualidade, confortável e durável. Tamanho {random.choice(sizes)}."
            stock = random.randint(10, 200)
            cost_price = Decimal(random.uniform(50, 100)).quantize(Decimal("0.01"))
            sale_price = Decimal(random.uniform(120, 250)).quantize(Decimal("0.01"))

            product = Product(
                name=name,
                description=description,
                active=True,
                category=category,
                stock=stock,
                cost_price=cost_price,
                sale_price=sale_price,
            )

            content = images_content.get(url)
            if content:
                ext = url.split(".")[-1]
                filename = f"{team.replace(' ', '-')}_{random.choice(kits)}_{i}.{ext}"
                product.image.save(filename, ContentFile(content))

            created_count += 1

            # Print de progresso a cada 100 produtos
            if (i + 1) % 100 == 0:
                self.stdout.write(
                    self.style.NOTICE(
                        f"Progresso: {i + 1}/{num_products} produtos criados..."
                    )
                )

        # Final
        self.stdout.write("\n")
        self.stdout.write(
            self.style.SUCCESS(f"✓ {created_count} produtos criados com sucesso!")
        )
        self.stdout.write(self.style.SUCCESS("Seed concluído com sucesso!"))
        self.stdout.write(
            self.style.SUCCESS(
                "Logins disponíveis:\n"
                "→ Admin: admin@exemplo.com / admin123\n"
                "→ Usuário normal: usuario@exemplo.com / user123"
            )
        )
