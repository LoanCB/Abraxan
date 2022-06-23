# Projet Abraxan

## Description
Projet annuel de deuxième année à l'ESGI Lyon, Abraxan a pour but de répondre à une réelle problématique de l'école : 
la gestion des contrats formateurs. <br>

Comme pour tout projet Django, Abraxan est divisé en modules afin de facilité son organisation. Actuellement, il ne 
possède que le module Nifleur servant à la gestion des contrats.

## Installation
### Récupération du projet
Tout d'abord, vous devez récupérer le projet en local. Si vous avez accès au github, vous pouvez le cloner en https avec 
la commande suivante :
```bash
git clone https://github.com/Patais/Abraxan.git
```
Vous pouvez également le télécharger et l'installer manuellement.

### Environnement virtuel
Il est conseillé d'utiliser un environnement virtuel pour le projet. Dans notre cas il s'agit de <u>virtualenv</u>. Je 
vous conseille de l'installer via la commande suivante :

```bash
pip install virtualenv
```
Il faut maintenant créer l'environnement virtuel via la commande suivante :
```bash
python3 -m venv /path/de/votre/environnement/virtuel 
```
A partir de maintenant, l'ensemble du projet se passera dans l'environnement virtuel créé à cet effet dans le dossier
venv. Pour activer ce dernier, il suffit de se rendre dans le dossier du projet ressemblant à ceci et de l'activer :
![img.png](static/images/readme/img.png)

- Windows :
```bash
.\venv\Scripts\activate
```

- Linux & macOs :
```bash
source venv/bin/activate
```

### Dépendances
Maintenant que votre environnement virtuel est activé, vous pouvez installer l'ensemble des dépendances. Pour facilité
cette dernière, un fichier requirements a été mis en place répertoriant l'ensemble des librairies.

```bash
pip install -r requirements.txt
```

### Clef secret & mot de passe
Pour des questions de sécurité, la clef secrète du serveur de django ainsi que le mot de passe de la base de données
sont stockées dans le fichier .env qui est propre à chaque machine. Vous devez donc créer ce fichier dans la racine du
projet et le renseigner de cette manière avec vos données : 
![img.png](static/images/readme/img_1.png)
<br>
<u>PS:</u> Pour la base de données, tout est expliqué juste en dessous.

### Base de données
#### Mise en place
Abraxan fonctionne sur une base de données Postgres SQL. Pour la faire fonctionner, il vous faudra l'installer en local:
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
<br>
Attention à bien garder le mot de passe que vous choisissez lors de l'installation de postgres !

Une fois l'installation effectuée, lancer pgAdmin et connectez vous. Ceci doit ressembler à cela :
![img_3.png](static/images/readme/img_3.png)
Ensuite, faites un clique droit sur base de données -> créer -> base de donnée puis créez une base se nomant 
"abraxan_dev".
Pour finir, vous devez renseigner le mot de passe dans le fichier .env créé juste avant.

#### Pycharm
Si vous utilisez l'IDE pycharm, vous pouvez ajouter la base de donnée à l'éditeur. Pour cela, cliquez sur le bouton 
Dabatase situé en haut à droite et cliquez sur le + -> Data Source -> PostgreSQL puis renseignez les paramètres : <br>
![img_2.png](static/images/readme/img_2.png)

N'hesitez à tester la connexion grâce au texte en bleu en bas.
<br>

#### Migrations
Une fois la base de données en place, il va falloir la migrer. Pour cela Django met en place une commande dans 
le manage.py :
```bash
python manage.py migrate
```

<u>Note de développement :</u> <br>
Si vous mettez à jour des modèles, n'oubliez pas de créer une nouvelle migration avec la commande suivante puis de 
migrer:
```bash
python manage.py makemigration
```

#### Compte
Pour finir avec la base de donnée, il est conseillé de créer un super utilisateur pour travailler en local
```bash
python manage.py createsuperuser
```

### Serveur
Maintenant que votre projet est prêt, il ne vous reste plus qu'à lancer le serveur :
```bash
python manage.py runserver
```
Une fois fait, vous pouvez vous rendre à l'addresse suivante : <b>127.0.0.1:8000</b>
<br>

<u>Note de développement :</u> <br>
Si vous éditez des fichiers python, il est nécessaire de redémarer le serveur pour appliquer les changements. Mais ne
vous inquietez pas, django le fait automatiquement pour vous !

## Support
Si vous rencontrez un problème, vous pouvez contacter un membre du groupe :
- Alexis Barreyre (Développeur logiciel) : alexis.barreyre@gmail.com
- Vincent Sosthene (Administrateur Systèmes & réseaux) : vincent.sosthene74@gmail.com
- Loan Courchinoux-Billonnet (Développeur Django) : loanbillonnet@gmail.com

## License
[MIT](https://choosealicense.com/licenses/mit/)
