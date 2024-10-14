# Generated by Django 4.2.11 on 2024-10-14 19:34

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import nxtbn.core.mixin
import nxtbn.core.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filemanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('meta_title', models.CharField(blank=True, help_text='Title for search engine optimization.', max_length=800, null=True)),
                ('meta_description', models.CharField(blank=True, help_text='Description for search engines.', max_length=350, null=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('meta_title', models.CharField(blank=True, help_text='Title for search engine optimization.', max_length=800, null=True)),
                ('meta_description', models.CharField(blank=True, help_text='Description for search engines.', max_length=350, null=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=7, unique=True)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Color',
                'verbose_name_plural': 'Colors',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published'), ('ARCHIVED', 'Archived')], default='DRAFT', max_length=20)),
                ('is_live', models.BooleanField(default=False)),
                ('meta_title', models.CharField(blank=True, help_text='Title for search engine optimization.', max_length=800, null=True)),
                ('meta_description', models.CharField(blank=True, help_text='Description for search engines.', max_length=350, null=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True)),
                ('internal_metadata', models.JSONField(blank=True, default=dict, null=True, validators=[nxtbn.core.models.no_nested_values])),
                ('metadata', models.JSONField(blank=True, default=dict, null=True, validators=[nxtbn.core.models.no_nested_values])),
                ('name', models.CharField(help_text='The name of the product.', max_length=255)),
                ('summary', models.TextField(help_text='A brief summary of the product.', max_length=500)),
                ('description', models.TextField(max_length=5000)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='product.category')),
                ('collections', models.ManyToManyField(blank=True, related_name='products_in_collection', to='product.collection')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('taxable', models.BooleanField(default=False)),
                ('physical_product', models.BooleanField(default=False)),
                ('track_stock', models.BooleanField(default=False)),
                ('has_variant', models.BooleanField(default=False)),
                ('weight_unit', models.CharField(blank=True, choices=[('GRAM', 'Gram'), ('KG', 'Kilogram'), ('LB', 'Pound'), ('OZ', 'Ounce'), ('TON', 'Ton')], max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('meta_title', models.CharField(blank=True, help_text='Title for search engine optimization.', max_length=800, null=True)),
                ('meta_description', models.CharField(blank=True, help_text='Description for search engines.', max_length=350, null=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('compare_at_price', models.DecimalField(blank=True, decimal_places=3, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('currency', models.CharField(choices=[('USD', 'United States Dollar'), ('EUR', 'Euro'), ('GBP', 'British Pound Sterling'), ('JPY', 'Japanese Yen'), ('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CHF', 'Swiss Franc'), ('CNY', 'Chinese Yuan'), ('SEK', 'Swedish Krona'), ('NZD', 'New Zealand Dollar'), ('INR', 'Indian Rupee'), ('BRL', 'Brazilian Real'), ('RUB', 'Russian Ruble'), ('ZAR', 'South African Rand'), ('AED', 'United Arab Emirates Dirham'), ('AFN', 'Afghan Afghani'), ('ALL', 'Albanian Lek'), ('AMD', 'Armenian Dram'), ('ANG', 'Netherlands Antillean Guilder'), ('AOA', 'Angolan Kwanza'), ('ARS', 'Argentine Peso'), ('AWG', 'Aruban Florin'), ('AZN', 'Azerbaijani Manat'), ('BAM', 'Bosnia and Herzegovina Convertible Mark'), ('BBD', 'Barbadian Dollar'), ('BDT', 'Bangladeshi Taka'), ('BGN', 'Bulgarian Lev'), ('BHD', 'Bahraini Dinar'), ('BIF', 'Burundian Franc'), ('BMD', 'Bermudian Dollar'), ('BND', 'Brunei Dollar'), ('BOB', 'Bolivian Boliviano'), ('BSD', 'Bahamian Dollar'), ('BTN', 'Bhutanese Ngultrum'), ('BWP', 'Botswana Pula'), ('BYN', 'Belarusian Ruble'), ('BZD', 'Belize Dollar'), ('CDF', 'Congolese Franc'), ('CLP', 'Chilean Peso'), ('COP', 'Colombian Peso'), ('CRC', 'Costa Rican Colón'), ('CUP', 'Cuban Peso'), ('CVE', 'Cape Verdean Escudo'), ('CZK', 'Czech Koruna'), ('DJF', 'Djiboutian Franc'), ('DKK', 'Danish Krone'), ('DOP', 'Dominican Peso'), ('DZD', 'Algerian Dinar'), ('EGP', 'Egyptian Pound'), ('ERN', 'Eritrean Nakfa'), ('ETB', 'Ethiopian Birr'), ('FJD', 'Fijian Dollar'), ('FKP', 'Falkland Islands Pound'), ('FOK', 'Faroese Króna'), ('GEL', 'Georgian Lari'), ('GGP', 'Guernsey Pound'), ('GHS', 'Ghanaian Cedi'), ('GIP', 'Gibraltar Pound'), ('GMD', 'Gambian Dalasi'), ('GNF', 'Guinean Franc'), ('GTQ', 'Guatemalan Quetzal'), ('GYD', 'Guyanese Dollar'), ('HKD', 'Hong Kong Dollar'), ('HNL', 'Honduran Lempira'), ('HRK', 'Croatian Kuna'), ('HTG', 'Haitian Gourde'), ('HUF', 'Hungarian Forint'), ('IDR', 'Indonesian Rupiah'), ('ILS', 'Israeli New Shekel'), ('IMP', 'Isle of Man Pound'), ('IQD', 'Iraqi Dinar'), ('IRR', 'Iranian Rial'), ('ISK', 'Icelandic Króna'), ('JMD', 'Jamaican Dollar'), ('JOD', 'Jordanian Dinar'), ('KES', 'Kenyan Shilling'), ('KGS', 'Kyrgyzstani Som'), ('KHR', 'Cambodian Riel'), ('KID', 'Kiribati Dollar'), ('KMF', 'Comorian Franc'), ('KRW', 'South Korean Won'), ('KWD', 'Kuwaiti Dinar'), ('KYD', 'Cayman Islands Dollar'), ('KZT', 'Kazakhstani Tenge'), ('LAK', 'Lao Kip'), ('LBP', 'Lebanese Pound'), ('LKR', 'Sri Lankan Rupee'), ('LRD', 'Liberian Dollar'), ('LSL', 'Lesotho Loti'), ('LYD', 'Libyan Dinar'), ('MAD', 'Moroccan Dirham'), ('MDL', 'Moldovan Leu'), ('MGA', 'Malagasy Ariary'), ('MKD', 'Macedonian Denar'), ('MMK', 'Burmese Kyat'), ('MNT', 'Mongolian Tögrög'), ('MOP', 'Macanese Pataca'), ('MRU', 'Mauritanian Ouguiya'), ('MUR', 'Mauritian Rupee'), ('MVR', 'Maldivian Rufiyaa'), ('MWK', 'Malawian Kwacha'), ('MXN', 'Mexican Peso'), ('MYR', 'Malaysian Ringgit'), ('MZN', 'Mozambican Metical'), ('NAD', 'Namibian Dollar'), ('NGN', 'Nigerian Naira'), ('NIO', 'Nicaraguan Córdoba'), ('NOK', 'Norwegian Krone'), ('NPR', 'Nepalese Rupee'), ('OMR', 'Omani Rial'), ('PAB', 'Panamanian Balboa'), ('PEN', 'Peruvian Sol'), ('PGK', 'Papua New Guinean Kina'), ('PHP', 'Philippine Peso'), ('PKR', 'Pakistani Rupee'), ('PLN', 'Polish Złoty'), ('PYG', 'Paraguayan Guaraní'), ('QAR', 'Qatari Riyal'), ('RON', 'Romanian Leu'), ('RSD', 'Serbian Dinar'), ('RWF', 'Rwandan Franc'), ('SAR', 'Saudi Riyal'), ('SBD', 'Solomon Islands Dollar'), ('SCR', 'Seychellois Rupee'), ('SDG', 'Sudanese Pound'), ('SGD', 'Singapore Dollar'), ('SHP', 'Saint Helena Pound'), ('SLL', 'Sierra Leonean Leone'), ('SOS', 'Somali Shilling'), ('SRD', 'Surinamese Dollar'), ('SSP', 'South Sudanese Pound'), ('STN', 'São Tomé and Príncipe Dobra'), ('SYP', 'Syrian Pound'), ('SZL', 'Eswatini Lilangeni'), ('THB', 'Thai Baht'), ('TJS', 'Tajikistani Somoni'), ('TMT', 'Turkmenistani Manat'), ('TND', 'Tunisian Dinar'), ('TOP', 'Tongan Paʻanga'), ('TRY', 'Turkish Lira'), ('TTD', 'Trinidad and Tobago Dollar'), ('TVD', 'Tuvaluan Dollar'), ('TWD', 'New Taiwan Dollar'), ('TZS', 'Tanzanian Shilling'), ('UAH', 'Ukrainian Hryvnia'), ('UGX', 'Ugandan Shilling'), ('UYU', 'Uruguayan Peso'), ('UZS', 'Uzbekistani Som'), ('VES', 'Venezuelan Bolívar Soberano'), ('VND', 'Vietnamese Đồng'), ('VUV', 'Vanuatu Vatu'), ('WST', 'Samoan Tālā'), ('XAF', 'Central African CFA Franc'), ('XCD', 'East Caribbean Dollar'), ('XOF', 'West African CFA Franc'), ('XPF', 'CFP Franc'), ('YER', 'Yemeni Rial'), ('ZMW', 'Zambian Kwacha'), ('ZWL', 'Zimbabwean Dollar')], default='USD', max_length=3)),
                ('price', models.DecimalField(decimal_places=3, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('cost_per_unit', models.DecimalField(decimal_places=3, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('track_inventory', models.BooleanField(default=False)),
                ('allow_backorder', models.BooleanField(default=False, help_text='Allow orders even if out of stock.')),
                ('stock', models.IntegerField(default=0, verbose_name='Stock')),
                ('low_stock_threshold', models.IntegerField(default=0, help_text='Threshold to trigger low stock alert.', verbose_name='Stock')),
                ('stock_status', models.CharField(choices=[('IN_STOCK', 'In Stock'), ('OUT_OF_STOCK', 'Out of Stock')], default='IN_STOCK', max_length=15)),
                ('sku', models.CharField(max_length=50, unique=True)),
                ('color_code', models.CharField(blank=True, max_length=7, null=True)),
                ('weight_unit', models.CharField(blank=True, choices=[('GRAM', 'Gram'), ('KG', 'Kilogram'), ('LB', 'Pound'), ('OZ', 'Ounce'), ('TON', 'Ton')], max_length=5, null=True)),
                ('weight_value', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('dimensions', models.CharField(blank=True, choices=[('MM', 'Millimeter'), ('CM', 'Centimeter'), ('M', 'Meter'), ('IN', 'Inch'), ('FT', 'Feet')], help_text='Format: Height x Width x Depth', max_length=50, null=True)),
                ('dimensions_value', models.CharField(blank=True, max_length=50, null=True)),
                ('attributes', models.JSONField(blank=True, default=dict, help_text='A JSON field to store custom attributes for the variant. Primary attributes include color code, dimension, and weight value. Weight value and dimension are used for shipping calculations. This field allows adding as many custom attributes as needed.', null=True, validators=[nxtbn.core.models.no_nested_values])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='product.product')),
                ('variant_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='filemanager.image')),
            ],
            options={
                'ordering': ('price',),
            },
            bases=(nxtbn.core.mixin.MonetaryMixin, models.Model),
        ),
    ]
