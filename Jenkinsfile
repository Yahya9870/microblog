pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'pip install -r requirements.txt' // Uncommented for actual build step
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'pytest tests/' // Uncommented for actual test step
            }
        }
        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube Analysis...'
                withSonarQubeEnv('SonarQube') {  // Ensure 'SonarQube' matches the server name in Jenkins
                    sh 'sonar-scanner' // Run SonarQube scanner
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Placeholder for deployment steps
            }
        }
    }
    post {
        always {
            echo 'Pipeline completed.'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
