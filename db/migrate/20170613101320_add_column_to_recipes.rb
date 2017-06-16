class AddColumnToRecipes < ActiveRecord::Migration
  def change
  	add_column :recipes, :recipes_name, :string
  	add_column :recipes, :ingredients, :string
  	add_column :recipes, :recipes_type, :boolean
  	add_column :recipes, :description, :text
  end
end
