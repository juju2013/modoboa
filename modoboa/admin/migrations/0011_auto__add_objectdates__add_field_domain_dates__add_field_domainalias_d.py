# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from modoboa.lib.compat import user_model_name


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ObjectDates'
        db.create_table('admin_objectdates', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modification', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('admin', ['ObjectDates'])

        # Adding field 'Domain.dates'
        db.add_column('admin_domain', 'dates', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['admin.ObjectDates']), keep_default=False)

        # Adding field 'DomainAlias.dates'
        db.add_column('admin_domainalias', 'dates', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['admin.ObjectDates']), keep_default=False)

        # Adding field 'Alias.dates'
        db.add_column('admin_alias', 'dates', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['admin.ObjectDates']), keep_default=False)

        # Adding field 'Mailbox.dates'
        db.add_column('admin_mailbox', 'dates', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['admin.ObjectDates']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'ObjectDates'
        db.delete_table('admin_objectdates')

        # Deleting field 'Domain.dates'
        db.delete_column('admin_domain', 'dates_id')

        # Deleting field 'DomainAlias.dates'
        db.delete_column('admin_domainalias', 'dates_id')

        # Deleting field 'Alias.dates'
        db.delete_column('admin_alias', 'dates_id')

        # Deleting field 'Mailbox.dates'
        db.delete_column('admin_mailbox', 'dates_id')


    models = {
        'admin.alias': {
            'Meta': {'object_name': 'Alias'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'dates': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.ObjectDates']"}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Domain']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extmboxes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mboxes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['admin.Mailbox']", 'symmetrical': 'False'})
        },
        'admin.domain': {
            'Meta': {'object_name': 'Domain'},
            'dates': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.ObjectDates']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quota': ('django.db.models.fields.IntegerField', [], {})
        },
        'admin.domainalias': {
            'Meta': {'object_name': 'DomainAlias'},
            'dates': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.ObjectDates']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Domain']"})
        },
        'admin.extension': {
            'Meta': {'object_name': 'Extension'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'admin.mailbox': {
            'Meta': {'object_name': 'Mailbox'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'dates': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.ObjectDates']"}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Domain']"}),
            'gid': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quota': ('django.db.models.fields.IntegerField', [], {}),
            'uid': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % user_model_name})
        },
        'admin.objectdates': {
            'Meta': {'object_name': 'ObjectDates'},
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
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
        user_model_name: {
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
        }
    }

    complete_apps = ['admin']
