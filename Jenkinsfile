pipeline {
  agent any
  stages {
    stage('Build stage') {
      environment {
        stageIP = '127.0.0.1'
        stageuser = 'admin'
        location = '/home/admmin/admin.com/'
      }
      steps {
        git(branch: 'staging', url: 'https://github.com/raj1rana/django-Tutorials-in-ppt.git')
        sh '''composer install && \\
        cp .env.example .env.testing && \\
        sed -i "s/DB_DATABASE=laravel/DB_DATABASE=$DB_DATABASE_SECURITY/g" .env.testing && \\
        sed -i "s/DB_PASSWORD=/DB_PASSWORD=$DB_PASSWORD_FAST_AUTH/g" .env.testing && \\
        sed -i "s/DB_USERNAME=root/DB_USERNAME=$DB_USERNAME_FAST_AUTH/g" .env.testing && \\
        sed -i "s/CAPTCHA_USE=true/CAPTCHA_USE=false/g" .env.testing && \\
	    . ./.env.testing && \\
        php artisan migrate:fresh --env=testing && \\
        composer run-script php-md && \\
        composer run-script phpcs && \\
        composer run-script test'''
      }
    }

    stage('BuildProduction') {
      environment {
        ProdIP = '27.30.25.121'
        produser = 'adminprod'
        locationprod = '/home/adminprod/admin.com'
      }
      steps {
        git(url: 'https://github.com/raj1rana/django-Tutorials-in-ppt.git', branch: 'master', changelog: true)
        sh '''rm -rf clone-folder && git clone --single-branch -b $BRANCH_NAME $GIT_URL clone-folder && \\
        cd clone-folder && \\
        git remote add aws-origin $AWS_COMMIT_ISM_FAST_LARAVEL_SECURITY && \\
        git push aws-origin $BRANCH_NAME && \\
        cd .. && rm -rf clone-folder && \\
        echo "update database in RDS" && \\
        cp .env.example .env && \\
        composer install && \\
        sed -i "s/DB_DATABASE=laravel/DB_DATABASE=${env.DB_DATABASE}/g" .env && \\
        sed -i "s/DB_PASSWORD=/DB_PASSWORD=${env.DB_PASSWORD}/g" .env && \\
        sed -i "s/DB_USERNAME=root/DB_USERNAME=${env.DB_USERNAME}/g" .env && \\
        sed -i "s/DB_HOST=127.0.0.1/DB_HOST=${env.DB_HOST}/g" .env && \\
        . ./.env && \\
        /usr/bin/php artisan key:generate && \\
        /usr/bin/php artisan migrate --seed && \\
        rm -rf .env && \\
        echo \'Deploy to ECS service started\' && \\
        aws cloudformation deploy --template-file ./cloudformation/fast-security-dev-service.yml \\
        --stack-name fast-security-dev-service --s3-bucket fast-security-dev-service \\
        --parameter-overrides TaskEcrImageUrl=${env.REPOSITORY_URI}:dev-${BUILD_NUMBER} \\
        --capabilities CAPABILITY_NAMED_IAM --no-fail-on-empty-changese --region us-east-2'''
      }
    }

  }
}