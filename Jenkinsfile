library 'deployment'

pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'git://github.com/dbazile/search.bazile.org'
            }
        }

        stage('Deploy') {
            steps {
                deployApplication('search')
            }
        }
    }
}
