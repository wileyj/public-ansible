include_recipe "apache"
package_name = 'jenkins'
service_name = 'jenkins'

execute "install_jenkins_repo" do
    command "wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat-stable/jenkins.repo"
    action :run
    not_if { ::File.exists?("/etc/yum.repos.d/jenkins.repo")}
end
execute "install_jenkins_key" do
    command "rpm --import http://pkg.jenkins-ci.org/redhat-stable/jenkins-ci.org.key"
    action :run
end

yum_package "java-1.6.0-openjdk" do
  action :install
  flush_cache [:before]
end

yum_package package_name do
  action :install
end

service service_name do
  action [ :enable, :start ]
end

template "/etc/httpd/conf.d/jenkins.conf" do
                source "jenkins.conf.erb"
                mode 0644
                owner "root"
                group "root"
                variables(
                                :servername   => "localhost",
				:jenkins_port => "8080"
                )
end

service "httpd" do
  action [ :restart ]
end
