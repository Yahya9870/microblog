pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'python3 --version'  // To verify the Python version
                sh 'pip3 install -r requirements.txt'  // Install dependencies
            }
        }
        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube Analysis...'
                withSonarQubeEnv('SonarQube') {  // Make sure this matches exactly
                    sh 'sonar-scanner'  // Run SonarQube scanner
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
