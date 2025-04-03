from django import forms


class CreateNewConsultorio(forms.Form):
    nombre = forms.CharField(label='Nombre:', max_length=100,
                             widget=forms.TextInput(attrs={'size': '40', 'placeholder': 'Nombre del consultorio'}))
    #  description = forms.CharField(widget=forms.Textarea(attrs={'class': 'input'}),
    #  required=False, label='DESCRIPCION:')


class CreateNewMedico(forms.Form):
    nombre = forms.CharField(label='Nombre:', max_length=100,
                             widget=forms.TextInput(attrs={'size': '40', 'placeholder': 'Nombre del médico'}))


class CreateNewProductos(forms.Form):
    nombre = forms.CharField(label='Nombre:',
                             widget=forms.TextInput(attrs={'size': '40', 'placeholder': 'Nombre del producto'}))
    descripcion = forms.CharField(label='Descripción:',
                                  widget=forms.Textarea(attrs={'cols': '50', 'rows': '5',
                                                               'placeholder': 'Descripción del producto'}))
    precio = forms.DecimalField(max_digits=10)


class CreateNewClientes(forms.Form):
    nombre = forms.CharField(label='Nombre:',
                             widget=forms.TextInput(attrs={'size': '40', 'placeholder': 'Nombre del cliente'}))
    apellido_paterno = forms.CharField(label='Apellido Paterno:',
                                       widget=forms.TextInput(attrs={'size': '40', 'placeholder': 'Apellido paterno'}))
    apellido_materno = forms.CharField(label='Apellido Materno:', required=False,
                                       widget=forms.TextInput(attrs={'size': '40', 'placeholder': 'Apellido materno'}))
    telefono1 = forms.CharField(label='Teléfono 1:',
                                widget=forms.TextInput(attrs={'size': '15', 'placeholder': 'Teléfono 1'}))
    telefono2 = forms.CharField(label='Teléfono 2:', required=False,
                                widget=forms.TextInput(attrs={'size': '15', 'placeholder': 'Teléfono 2'}))
    correo = forms.CharField(label='Correo:', required=False,
                             widget=forms.TextInput(attrs={'size': '30', 'placeholder': 'Correo'}))
    codigo_postal = forms.CharField(label='Código Postal:', required=False,
                                    widget=forms.TextInput(attrs={'size': '12', 'placeholder': 'Código Postal'}))
    calle = forms.CharField(label='Dirección:', required=False,
                            widget=forms.TextInput(attrs={'size': '40', 'placeholder': 'Calle'}))
    numero_ext = forms.CharField(label='Núm.Exterior:', required=False,
                                 widget=forms.TextInput(attrs={'size': '12', 'placeholder': 'Núm.Exterior'}))
    numero_int = forms.CharField(label='Núm.Interior:', required=False,
                                widget=forms.TextInput(attrs={'size': '12', 'placeholder': 'Núm.Interior'}))
    fecha_nac = forms.DateField(label='Fecha Nacimiento:', required=False,
                                 widget=forms.TextInput(attrs={'size': '12', 'placeholder': 'Fecha Nacimiento'}))
    rfc = forms.DateField(label='RFC:', required=False,
                                 widget=forms.TextInput(attrs={'size': '13', 'placeholder': 'RFC'}))