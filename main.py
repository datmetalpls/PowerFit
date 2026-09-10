"""PowerFit - Punto de entrada principal."""
from persona import Persona
from direccion import Direccion
from comuna import Comuna
import uuid

Usuario=Persona("2111111-K", "César", "Guerrero", "Acevedo", "+56333434342", "correo@notiene.cl")
comu_ine=Comuna(4105, "Paihuano")

print (Usuario.getRut())
print (Usuario.getNombres())

id_autogenerado=str(uuid.uuid4())
domicilio=Direccion(id_autogenerado ,"Casa","Ramon Venegas",3116,"El parque")

print ("ID: ", domicilio.getIdDireccion() ,"\n", "Calle:", domicilio.getCalle(),"\n", "Número: ", domicilio.getNumero(),"\n", "Calle Referencia: ", domicilio.getReferencia())

print(domicilio.getIdDireccion())

print(comu_ine())

