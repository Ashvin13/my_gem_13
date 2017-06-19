class Recipe < ActiveRecord::Base
	attr_accessible :recipes_name, :ingredients, :recipes_type, :description, :email
	belongs_to :user
end
