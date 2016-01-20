package_name = 'httpd'
service_name = 'httpd'
document_root = '/var/www/html'

yum_package package_name do
   action :install
   flush_cache [:before]
end

service service_name do
  action [ :enable, :start ]
end

