class Recipe < ActiveRecord::Base
	attr_accessible :recipes_name, :ingredients, :recipes_type, :description, :email, :image, :remote_image_url, :user_id
	belongs_to :user
	mount_uploader :image, ImageUploader

	searchkick word_start: [:recipes_name, :description]

	def search_data
	    {
	      recipes_name: recipes_name,
	      description: description
	    }
  	end

	# def self.search(search)
	#   if search
	#     where("recipes_name like ?", "%#{search}%")
	#   else
	#     find(:all)
	#   end
	# end
end
