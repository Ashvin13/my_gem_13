class AddEmailToRecipes < ActiveRecord::Migration
  def change
    add_column :recipes, :email, :string
  end
end
