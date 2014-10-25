class UsersController < ApplicationController
    def new
        @user = User.new
    end

    def create
        @user = User.new(article_params)
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

    private
        def article_params
            params.require(:user).permit(:label, :name, :surname)
        end
end


