class Ability
  include CanCan::Ability

  def initialize(user)
    user ||= User.new

    if user.role? == true
        can :manage, :all
    else
        can [:read, :create], Recipe
        can [:update, :destroy], Recipe, :user_id => user.id
    end
  end
end
