class Recipe < ActiveRecord::Base
	attr_accessible :recipes_name, :ingredients, :recipes_type, :description, :email, :image, :remote_image_url, :user_id
	belongs_to :user
	mount_uploader :image, ImageUploader

	searchkick word_start: [:recipes_name, :description]

	validates_presence_of :recipes_name
	validates_presence_of :email

	def search_data
	    {
	      recipes_name: recipes_name,
	      description: description
	    }
  	end

  	def self.mail_recap_semaine
  		@recipe = Recipe.all
  		@recipe.each do |r|
      		UserMailer.mail_recap_semaine(r.email).deliver
    	end
  	end
end
