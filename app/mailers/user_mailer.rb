class UserMailer < ApplicationMailer
	default from: "itserviceyouth@gmail.com"
	def new_recipe_email(email)
		@recipe_email = email
		mail(to: @recipe_email, subject: 'For a new product')
	end

	def contact_email(name, email, message)
		@user_name = name
		@user_email = email
		@user_msg = message
		mail(to: "ashvinptel@gmail.com", subject: "contact us form")
	end

	def mail_recap_semaine(email)
		mail(:to => email, :subject => "Weekly email from footyaddicts")
	end
end
