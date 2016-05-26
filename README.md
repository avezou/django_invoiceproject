# Django InvoiceProject

This is a Django project aimed at individuals and small businesses that are
looking for a simple way to invoice their customers.

This sample project is aimed at a small pet services business, so the
models and apps are customized for that use case. Anything can be rewritten to
fit other use cases. The invoiceapp relies on Service, Pet, Customer, and
Address. As of now, Address is the only published app. It can be installed with
pip install django-simple-address (address in INSTALLED_APPS). I do not plan on
publishing the services or pets apps as they are very simple and specific to
my current use case. I may publish them bundled with the invoiceapp as it is
dependent on them.

## Installation

To install the project clone the repository or download the project as a zip and
extract it. Change to the django_invoiceproject
directory, and install the requirements with
`pip install -r requirements.txt`. Make sure this is done in a virtualenv.

Postfix is used to email customers the invoices.

Make sure that postfix is installed and configured.

For Ubuntu systems:
`sudo apt-get install postfix` will install it.

To configure it:
`cp /usr/share/postfix/main.cf.debian /etc/postfix/main.cf`
Add the following lines to main.cf:

`mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128`
`mydestination = localhost`

Then, reload this config file: `/etc/init.d/postfix reload`

For more information checkout the postfix documentation

Test that you can send email from the command line.
If this is successfull, you are all done for sending emails

Lastly, configure your postgres database.
This project assume that you have created a directory called otm unser /etc/
and created a pass and secret files containing your db user password and your
djangi secret key respectively. So, the db user password is under `/etc/otm/pass`
and the secret key is at `/etc/otm/secret`
If you want to change the email host and information, change the configuration
in the settings.py file


## Usage

Once all the required packaged are installed in virtualenv and postfix setup
Run: `python manage.py migrate` to create the database tables
Then create a superuser: `python mange.py createsuperuser`,
Finally run the development server: `python manage.py runserver`
Then go to localhost:8000/admin. Login with the super user credentials,
you should be able to add your business information, and other goodies.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D



## License

Look at the [LICENSE](LICENSE) file at the root of the project
