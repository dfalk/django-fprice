# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Section'
        db.delete_table('fprice_section')

        # Adding model 'ProductCategory'
        db.create_table('fprice_productcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['fprice.ProductCategory'])),
        ))
        db.send_create_signal('fprice', ['ProductCategory'])

        # Deleting field 'Product.section'
        db.delete_column('fprice_product', 'section_id')

        # Adding field 'Product.category'
        db.add_column('fprice_product', 'category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fprice.ProductCategory'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Section'
        db.create_table('fprice_section', (
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', null=True, to=orm['fprice.Section'], blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, db_index=True)),
        ))
        db.send_create_signal('fprice', ['Section'])

        # Deleting model 'ProductCategory'
        db.delete_table('fprice_productcategory')

        # Adding field 'Product.section'
        db.add_column('fprice_product', 'section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fprice.Section'], null=True, blank=True), keep_default=False)

        # Deleting field 'Product.category'
        db.delete_column('fprice_product', 'category_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fprice.price': {
            'Meta': {'ordering': "['-last_time_update']", 'object_name': 'Price'},
            'currency': ('django.db.models.fields.CharField', [], {'default': "'rur'", 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_time_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_user_update': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_user_update'", 'to': "orm['auth.User']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fprice.Product']"}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fprice.Shop']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'update_counter': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'fprice.product': {
            'Meta': {'ordering': "['title']", 'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fprice.ProductCategory']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'fprice.productcategory': {
            'Meta': {'ordering': "['title']", 'object_name': 'ProductCategory'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['fprice.ProductCategory']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'fprice.shop': {
            'Meta': {'ordering': "['title']", 'object_name': 'Shop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'fprice.trade': {
            'Meta': {'ordering': "['-time']", 'object_name': 'Trade'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fprice.Price']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['fprice']
