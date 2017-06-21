class RecipesController < ApplicationController
  before_action :set_recipe, only: [:show, :edit, :update, :destroy]
  load_and_authorize_resource
  # GET /recipes
  # GET /recipes.json
  # def index
  #   @recipes = Recipe.all
  #   if params[:search]
  #     @recipes = Recipe.search(params[:search])
  #   else
  #     @recipes = Recipe.all.order('created_at DESC')
  #   end
  # end

  def index
    search = params[:search].present? ? params[:search] : nil
    @recipes = if search
       Recipe.where("recipes_name LIKE ? OR description LIKE ?", "%#{search}%", "%#{search}%") 
     else
       Recipe.all
    end
  end


  def autocomplete
    render json: Recipe.search(params[:query], {
      fields: ["recipes_name^5", "description"],
      match: :word_start,
      limit: 10,
      load: false,
      misspellings: {below: 5}
    }).map(&:recipes_name)
  end

  # GET /recipes/1
  # GET /recipes/1.json
  def show
  end

  # GET /recipes/new
  def new
  end

  # GET /recipes/1/edit
  def edit
  end

  # POST /recipes
  # POST /recipes.json
  def create
    @user = current_user
    @recipe = @user.recipes.new(recipe_params)
    respond_to do |format|
      if @recipe.save
        format.html { redirect_to @recipe, notice: 'Recipe was successfully created.' }
        format.json { render :show, status: :created, location: @recipe }
        UserMailer.delay(run_at: 2.minutes.from_now).new_recipe_email(@recipe.email)
      else
        format.html { render :new }
        format.json { render json: @recipe.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /recipes/1
  # PATCH/PUT /recipes/1.json
  def update
    respond_to do |format|
      if @recipe.update(recipe_params)
        format.html { redirect_to @recipe, notice: 'Recipe was successfully updated.' }
        format.json { render :show, status: :ok, location: @recipe }
      else
        format.html { render :edit }
        format.json { render json: @recipe.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /recipes/1
  # DELETE /recipes/1.json
  def destroy
    @recipe.destroy
    respond_to do |format|
      format.html { redirect_to recipes_url, notice: 'Recipe was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_recipe
      @recipe = Recipe.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def recipe_params
      params.require(:recipe).permit(:recipes_name, :ingredients, :recipes_type, :description, :email, :user_id, :image)
    end
end
