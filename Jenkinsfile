pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                // Install dependencies
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing...'
                // Run tests
                sh 'pytest tests/'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                // Run SonarQube analysis
                // Note: Ensure that the SonarQube plugin and server are configured in Jenkins
                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Placeholder for deployment commands
                // Uncomment and add actual deployment commands
                // sh 'your_deployment_command_here'
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
            // Add any cleanup or final steps here if needed
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
