"""PowerFit - Punto de entrada principal."""
from src.models import Persona, Direccion, cargar_comunas_ine
import uuid

Usuario=Persona("2111111-K", "César", "Guerrero", "Acevedo", "+56333434342", "correo@notiene.cl")
comu_ine=cargar_comunas_ine()

print (Usuario.getRut())
print (Usuario.getNombres())

id_autogenerado=str(uuid.uuid4())
domicilio=Direccion(id_autogenerado ,"Casa","Ramon Venegas",3116,"El parque")

print ("ID: ", domicilio.getIdDireccion() ,"\n", "Calle:", domicilio.getCalle(),"\n", "Número: ", domicilio.getNumero(),"\n", "Calle Referencia: ", domicilio.getReferencia(), "Comuna: ", comu_ine.get(13101))