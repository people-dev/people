require 'test_helper'

class UserTest < ActiveSupport::TestCase
    setup do
        @user = User.new(label: "12musterm", password: "foobar", password_confirmation: "foobar")
    end

    test "should be valid by default" do
        assert @user.valid?
    end

    test "label should have a max length of 8" do
        @user.label = "12mustermann"
        assert_not @user.valid?
        @user.label = "12leet"
        assert @user.valid?
        @user.label = "12musterm"
        assert @user.valid?
    end

    test "user should have a label" do
        @user.label = nil
        assert_not @user.valid?
    end

    test "password should have a minimum length" do
        assert @user.valid?
        @user.password = @user.password_confirmation = "a" * 5
        assert_not @user.valid?
    end

    test "labels should be unique" do
        duplicate_user = @user.dup
        duplicate_user.label = @user.label.upcase
        @user.save
        assert_not duplicate_user.valid?
    end
end
