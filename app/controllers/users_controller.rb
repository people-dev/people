class UsersController < ApplicationController
    def new
        @user = User.new
    end

    def create
        @user = User.new(user_create_params)
        if @user.save
            redirect_to @user
        else
            render "new"
        end
    end

    def show
        @user = User.find(params[:id])
    end

    def index
        render plain: "Indexing disabled"
    end

    def edit
        @user = User.find(params[:id])
    end

    def update
        @user = User.find(params[:id])

        if @user.update(user_edit_params)
            redirect_to @user
        else
            render 'edit'
        end
    end

    private
        def user_create_params
            params.require(:user).permit(:label, :name, :surname, :password, :password_confirmation)
        end

        def user_edit_params
            params.require(:user).permit(:name, :surname, :age, :major, :gender)
        end
end


