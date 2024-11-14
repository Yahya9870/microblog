pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'pytest tests/'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Placeholder for actual deployment steps
                // sh 'your_deployment_command_here'
            }
        }
    }
}
