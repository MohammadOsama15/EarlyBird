# Deployment Setup

## Steps to deploy:
    1. Install fly in linux using the command - "curl -L https://fly.io/install.sh | sh"
    2. If you want to signup - "fly auth signup"
    3. If you want to login - "fly auth login"
    4. Launch the app using the command "fly launch"
        1. Set up the app name
        2. Choose the region 
        3. Choose if you want a postgres database
        4. Choose if you want a redis database 
    5. Then deploy the app "fly deploy"

## If you want to check the connection/health of your instance:
    - flyctl doctor
    - flyctl status
    - for more detailed status about a machine use the command - fly machine status <machine id>

## If the app is having issues connecting due to slow internet speed, try the following commands:
    - flyctl wireguard reset
    - flyctl agent restart
    - flyctl websocket enable

## If you want to increase the space of the app:
    - fly scale -a "app name" memory <space in mbs>

## If you want to destroy the app use the following command:
    - flyctl destroy "app name"

## To open ssh console:
    - fly ssh module "app name"

## Deployed address:
    - reddit-sentiment-analyzer.fly.dev

## In order to avoid the DB not binding error use:
    - In fly.toml change the builder from builder = "paketobuildpacks/builder:base" to builder = "paketobuildpacks/builder:full"
