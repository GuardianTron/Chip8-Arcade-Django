from django.db.models.fields.files import FieldFile,FileField

class Chip8FieldFile(FieldFile):

    def save(self, name,content,save=True):
        '''convent file into hex text format for extra security.'''
        content_converted = content.file.read().hex().encode()
        content.file.seek(0)
        content.file.write(content_converted)
        
        super().save(name,content,save)

class Chip8FileField(FileField):

    attr_class = Chip8FieldFile    