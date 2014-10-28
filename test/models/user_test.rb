require 'test_helper'

class UserTest < ActiveSupport::TestCase
    setup do
        @user = User.new(label: "12musterm", password: "foobar", password_confirmation: "foobar")
    end

    test "label should have a max length of 8" do
        @user.label = "12mustermann"
        assert_not @user.valid?
        @user.label = "12leet"
        assert @user.valid?
        @user.label = "12musterm"
        assert @user.valid?
    end

    test "password should have a minimum length" do
        assert @user.valid?
        @user.password = @user.password_confirmation = "a" * 5
        assert_not @user.valid?
    end
end
