pipeline {
    agent {
        node {
            label 'Agent01'
        }
    }
    options {
        // Ensures job runs to completion even with minor non-fatal errors 
        skipDefaultCheckout() 
    }

    environment {
        BRANCH_NAME = "main"
        // Create credentials in Jenkins for security
        TWINE_PASSWORD = credentials('pypi-token')
        RENOPSAPI_KEY = credentials('RENOPSAPI_KEY')
        TWINE_USERNAME = "__token__" 
    }

    stages {
        
        stage('Checkout') {
          steps {
              echo 'Checkout SCM'
              checkout scm
            }
        }
        stage("Clean"){
            steps{
                script {
                    echo "Cleaning"
                    sh "rm -rf dist"
                }
            }
        }
        stage("Build"){
            steps{
                script {
                    echo "Building"
                    sh "ls -all"
                    sh "python -V"
                    sh "pip install virtualenv"
                    sh "virtualenv venv"
                    sh "source venv/bin/activate"
                    sh "pip install build"
                    sh "python -m build"
                }
            }
        }

    
        stage('Publish') {
            steps {
                sh '''
                    pip install twine
                    python -m twine upload --verbose --repository-url https://upload.pypi.org/legacy/ dist/* 
                '''
            }
        } 
        stage('Test') {
            steps {
                script {
                    sh '''
                        pip install renops-scheduler
                        echo 'print("hello world!")' > test.py
                        renops-scheduler test.py -la -r 1 -d 1 --optimise-price # Test prices
                    ''' 
                }
            }
        }   
    }
}
