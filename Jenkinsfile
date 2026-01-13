pipeline {
    agent any

    stages  {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/tinNguyen05/Two-Tier-Flask-App.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t two-tier-flask-app:latest .'
            }
        }

        stage('Deploy with docker-compose') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'
            }
        }
    }

}