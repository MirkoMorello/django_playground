from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
     class Meta(BaseUserCreateSerializer.Meta):
         fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name'] # abbiamo fatto override solo di fields, aggiungendo first_name, last_name, così adesso nella creazione in post vengono richiesti