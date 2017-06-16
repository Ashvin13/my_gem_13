class UserMailer < ApplicationMailer
	default from: "support@nestbuddy.com"
	def new_recipe_email(email)
		@recipe_email = email
		mail(to: @recipe_email, subject: 'For a new product')
	end
end
