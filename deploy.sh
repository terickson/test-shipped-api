#! /bin/sh

# define hosts to deploy to

case $1 in   
    -azure)
        user="hackathon"
        hosts=("ciscoHackathon2016.cloudapp.net")
        serviceSetupCommand="sudo update-rc.d hackathon-api defaults"
        sudoCmd="sudo "
        monitDir="/etc/monit/conf.d/"
        ;;
    *)
        echo "please run with $0 -prod"
        exit 1
esac

for i in ${hosts[@]}; do
    ssh ${user}@${i} "cd /var/services/hackathon-api; git pull";
    ssh ${user}@${i} "cd /var/services/hackathon-api; ${sudoCmd}pip3 install -r requirements.txt"
    ssh ${user}@${i} "${sudoCmd}cp -f /var/services/hackathon-api/init.d/hackathon-api /etc/init.d/"
    ssh ${user}@${i} ${serviceSetupCommand}
    ssh ${user}@${i} "${sudoCmd}/etc/init.d/hackathon-api stop"
    ssh ${user}@${i} "${sudoCmd}rm -f /var/services/hackathon-api/app.pid"
    ssh ${user}@${i} "${sudoCmd}cp -f /var/services/hackathon-api/monit.d/hackathon-api ${monitDir}"
    ssh ${user}@${i} "${sudoCmd}service monit reload"
done
