pipeline {
  agent 'any'
  options {
    skipStagesAfterUnstable()
    disableConcurrentBuilds()
  }

 

  stages {

    // Build and test cases
    stage('BuildAndTest') {
      when {
        branch '*'
      }
      steps {
        echo 'Build started'
        sh """
        composer install && \
        cp .env.example .env.testing && \
        sed -i "s/DB_DATABASE=laravel/DB_DATABASE=$DB_DATABASE_SECURITY/g" .env.testing && \
        sed -i "s/DB_PASSWORD=/DB_PASSWORD=$DB_PASSWORD_FAST_AUTH/g" .env.testing && \
        sed -i "s/DB_USERNAME=root/DB_USERNAME=$DB_USERNAME_FAST_AUTH/g" .env.testing && \
        sed -i "s/CAPTCHA_USE=true/CAPTCHA_USE=false/g" .env.testing && \
	    . ./.env.testing && \
        php artisan migrate:fresh --env=testing && \
        composer run-script php-md && \
        composer run-script phpcs && \
        composer run-script test
        """
      }
  }

// Build Development
    stage('BuildDevelopment') {
      when {
        branch 'dev'
      }
      steps {
        echo 'Api-documentation auto-generate'
        sh """
        composer install
        php artisan apidoc:generate
        """
        echo 'build started'
        // Build steps goes here for dev build
        sh """
        eval \$(aws ecr get-login --no-include-email --region us-east-2)
        docker build -t ${env.REPOSITORY_URI}:dev-${BUILD_NUMBER} . --build-arg GITHUB_PERSONAL_TOKEN=${GITHUB_PERSONAL_TOKEN}
        docker push ${env.REPOSITORY_URI}:dev-${BUILD_NUMBER}
        echo docker image push successfully
        """
        //Build steps goes here for dev worker build
        sh """
        eval \$(aws ecr get-login --no-include-email --region us-east-2)
        docker build . -f worker.Dockerfile -t ${env.REPOSITORY_URI}:dev-worker-${BUILD_NUMBER} --build-arg GITHUB_PERSONAL_TOKEN=${GITHUB_PERSONAL_TOKEN}
        docker push ${env.REPOSITORY_URI}:dev-worker-${BUILD_NUMBER}
        echo docker image push successfully
        """
      }
    }

  // Build Staging
    stage('BuildStging') {
      when {
        branch 'staging'
      }
      steps {
        // Build steps for staging build
        echo 'build started'
      }
    }

    // Build Production
    stage('BuildProduction') {
      when {
        branch 'master'
      }
      steps {
        // Build steps goes here
        echo 'build started'
      }
    }

    // Deploy Development
    stage('DeployDevelopment') {
      when {
        branch 'dev'
      }
      steps {
        //deploy steps goes here
        echo 'Sync Codecommit Repo Started'
        sh """
        rm -rf clone-folder && git clone --single-branch -b $BRANCH_NAME $GIT_URL clone-folder && \
        cd clone-folder && \
        git remote add aws-origin $AWS_COMMIT_ISM_FAST_LARAVEL_SECURITY && \
        git push aws-origin $BRANCH_NAME && \
        cd .. && rm -rf clone-folder && \
        echo "update database in RDS" && \
        cp .env.example .env && \
        composer install && \
        sed -i "s/DB_DATABASE=laravel/DB_DATABASE=${env.DB_DATABASE}/g" .env && \
        sed -i "s/DB_PASSWORD=/DB_PASSWORD=${env.DB_PASSWORD}/g" .env && \
        sed -i "s/DB_USERNAME=root/DB_USERNAME=${env.DB_USERNAME}/g" .env && \
        sed -i "s/DB_HOST=127.0.0.1/DB_HOST=${env.DB_HOST}/g" .env && \
        . ./.env && \
        /usr/bin/php artisan key:generate && \
        /usr/bin/php artisan migrate --seed && \
        rm -rf .env && \
        echo 'Deploy to ECS service started' && \
        aws cloudformation deploy --template-file ./cloudformation/fast-security-dev-service.yml \
        --stack-name fast-security-dev-service --s3-bucket fast-security-dev-service \
        --parameter-overrides TaskEcrImageUrl=${env.REPOSITORY_URI}:dev-${BUILD_NUMBER} \
        --capabilities CAPABILITY_NAMED_IAM --no-fail-on-empty-changese --region us-east-2
      """
      }
    }
    // Deploy Dev Worker
    stage('DeployWorker') {
      when {
        branch 'dev'
      }
      steps {
        //deploy steps goes here
        sh """
        echo 'Deploy to ECS service started' && \
        aws cloudformation deploy --template-file ./cloudformation/fast-security-worker-dev-service.yml \
        --stack-name fast-security-worker-dev-service --s3-bucket fast-security-worker-dev-service \
        --parameter-overrides TaskEcrImageUrl=${env.REPOSITORY_URI}:dev-worker-${BUILD_NUMBER} \
        --capabilities CAPABILITY_NAMED_IAM --no-fail-on-empty-changeset --region us-east-2
      """
      }
    }
    // Deploy Staging
    stage('DeployStaging') {
      when {
        branch 'staging'
      }
      steps {
        //deploy steps goes here
        echo 'deploy started'
      }
    }

    // Production Deployment
    stage('DeployProduction') {
      when {
        branch 'master'
      }
      steps {
        //deploy steps goes here
        echo 'deploy started'
      }
    }
  }
  post {
        failure {
            emailext attachLog: true, attachmentsPattern: 'phpcs-report.xml , phpmd-report.html',
            body: "${currentBuild.currentResult}: Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\n More info at: ${env.BUILD_URL}",
            to: "${DEVELOPER_EMAIL}",
            recipientProviders: [developers(), requestor()],
            subject: "Jenkins Build ${currentBuild.currentResult}: Job ${env.JOB_NAME}"
          }
        always {
          cleanWs()
      }
    }

}
