# linkliv
We followed the requirements, using Flask as the backend.  
This project has already been deployed on Heroku to facilitate the grading process.  
https://linkliv-1214-8c0efb304be3.herokuapp.com/  
We also provide a video as required, in case the database does not work on your end.  
https://drive.google.com/file/d/1jnnvSqOV4iyLcsEKykYNHNLrvY-SAzJp/view?usp=sharing  

## Install Required Packages
pip install -r requirements.txt

## PostgreSQL Database Setup
Ensure PostgreSQL is installed and running on your system. If not, install PostgreSQL:

### On Ubuntu/Debian:
sudo apt-get update 
sudo apt-get install postgresql postgresql-contrib 

### On macOS (using Homebrew):
brew install postgresql 
brew services start postgresql 

## Create a new PostgreSQL database and user (replace 'username' and 'password' with your desired values):
sudo -u postgres psql 
CREATE DATABASE linklivdb; 
CREATE USER username WITH ENCRYPTED PASSWORD 'password';  
GRANT ALL PRIVILEGES ON DATABASE linklivdb TO username;  
\q 

## Set Environment Variables

export DATABASE_URL="postgresql://username:password@localhost/linklivdb" or change in app.py  

## Running the Application

python3 app.py  


This app includes the following routes:  

Home: http://127.0.0.1:5000/   
Profile Show: http://127.0.0.1:5000/profile/show  
Profile Edit: http://127.0.0.1:5000/profile/edit  
Compare: http://127.0.0.1:5000/compare    
Filter: http://127.0.0.1:5000/filter  
Scan & Share: http://127.0.0.1:5000/add  
Login: http://127.0.0.1:5000/login  

Please press F12 in your browser and click on the mobile icon to switch to mobile view for testing. 
