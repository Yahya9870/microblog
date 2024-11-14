pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'python3 --version'  // To verify the Python version
                sh 'python3 -m pip install --user -r requirements.txt'  // Use python3 -m pip for a consistent environment
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'python3 -m pytest tests/'  // Use python3 to invoke pytest
            }
        }
        stage('SonarQube Analysis') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo 'Running SonarQube Analysis...'
                withSonarQubeEnv('SonarQube') {  // Ensure 'SonarQube' matches the server name configured in Jenkins
                    sh 'sonar-scanner'  // Run SonarQube scanner
                }
            }
        }
        stage('Deploy') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
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
