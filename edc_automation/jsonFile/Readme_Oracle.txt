Data: 21 luglio

Di seguito le variabili definite per la Risorsa:

## Oracle

$SourceConnectionName	
$ResourceName	
$UserMetadati	
$PasswordUserMetadati
$UserDatiMetadati  			-> servono solo per la Connessione Infa - No EDC
$PasswordUserDatiMetadati	-> servono solo per la Connessione Infa - No EDC
$FlagConnectString			-> Se valorizzato a NO bisogna usare Host e Port
							Se valorizzato a SI bisognare usare la ConnectString
$Host	
$Port						-> Nel caso di ConnectString il template contiene un valore dummy (1521)
$Service
$ConnectStringResource	
$ConnectStringDiscovery
$Database	
$EnableSourceMetadata 	
$SamplingOption 	
$RandomSamplingRows	
$ExcludeViews			-> Occhio che è un boolean
$Cumulative 	
$DataDomainGroups	-> si possono presentare più valori separati da una virgola (nel JSON devono avere i doppi apici)
$ExcludeNullValues	
$RunSimilarityProfile


