import BAC0
import netifaces
import ipaddress


from BAC0.core.devices.Device import DeviceProperties


nombre_de_valeurs = int
device_nb = int
device_nb = 0

#Detection de l'adresse IP et allocution à une variable qui s'appelle eth0_address
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Trouver toutes les interfaces réseau disponibles
interfaces = netifaces.interfaces()

# Rechercher l'adresse IP et le masque de sous-réseau associés à la carte eth0
eth0_address = None
eth0_netmask = None
eth0_ip = None
for iface in interfaces:
    if iface == "eth0":
        addresses = netifaces.ifaddresses(iface)
        eth0_address = addresses[netifaces.AF_INET][0]["addr"]
        eth0_netmask = addresses[netifaces.AF_INET][0]["netmask"]
       
        break
        

# Vérifier si l'adresse et le masque de sous-réseau ont été trouvés et les stocker dans des variables
if eth0_address and eth0_netmask:
    network = ipaddress.IPv4Network(f'{eth0_address}/{eth0_netmask}', strict=False)
    eth0_ip = addresses[netifaces.AF_INET][0]["addr"]+"/"+str(network.prefixlen)
    
else:
    print("Adresse IP et/ou masque de sous-réseau de la carte eth0 introuvable(s)")
	
# Connexion à l'automate
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

bacnet = BAC0.lite(eth0_ip)  #connexion a l'automate

    
ip, device_id = bacnet.whois()[0]#récupération de son ip et id
#print(ip)
#print(device_id)
#print(bacnet.devices)			#print pour vérification



#Création du tableau dynamique du nombre d'appareil trouvé
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

devices = bacnet.whois()


tableau = []

# Boucle sur la liste des appareils et stockage des adresses IP et IDs de périphérique dans le tableau
for device in devices:
    ip = device[0]
    device_id = device[1]
    tableau.append([ip, device_id])
    device_nb +=1;

# Affichage du tableau
nombre_de_valeurs = len(tableau)

print ("il y a",nombre_de_valeurs ,"appareils détectés")
print(bacnet.devices)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# Création de l'instance de DeviceProperties
ip, device_id = bacnet.whois()[0]


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#Récupération des data et écriture dans plusieurs fichiers "values"
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

ip = '169.254.45.143'

#ouverture du fichier qui va reccueillir les donnees
tab = []
i = int
# Lire les valeurs de l'objet et les stocker dans un tableau à deux colonnes
#for objet in
tab = bacnet.read(f'{device[0]} device {device[1]} objectList')
nombre_de_lignes = len(tab)
# Initialisation des tableaux vides
object_type_tab = []
object_id_tab = []

# Boucle for pour extraire les valeurs de chaque paire
fichier = open('objecttype+objectid', 'w')
for pair in tab:
    object_type_value = pair[0]
    object_id_value = pair[1]
    #ajout des valeurs au tableau
    object_type_tab.append(object_type_value)
    object_id_tab.append(object_id_value)
    
    object_id_value_str = str(object_id_value)
    fichier.write(object_type_value+"   "+object_id_value_str+'\n')
    
    c=len(object_type_tab)
    d=len(object_id_tab)
    print(c,d)
#print(object_type_tab)
#print(object_id_tab)

#ip = '169.254.45.143'

long_tab=len(tab)

for device in devices:
	converted_id = str(device[1])
	fichier = open('presentValue', 'w')#'device_'+converted_id+'_valuestest2', 'w')
	
for i in range (long_tab):
	try:
		data = bacnet.read(f'{ip} {object_type_tab[i]} {object_id_tab[i]}  presentValue')
		i+=1
		print(data)
		str_data = str(data)		#conversion des data en string

		fichier.write("presentValue = "+str_data+' \n ')#ecriture des donnees dans le fichier
		
	except BAC0.core.io.IOExceptions.UnknownPropertyError:
        # si la propriété presentValue n'est pas disponible, ignorer et continuer à la prochaine itération
        	fichier.write("Pas de presentValue"' \n ')
       		i+=1
fichier.close()			#fermeture du fichier
	


