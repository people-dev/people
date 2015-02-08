require 'test_helper'

class UserSignupTest < ActionDispatch::IntegrationTest
    test 'invalid signup information' do
        get signup_path
        assert_no_difference 'User.count' do
            post users_path, user: {
                label: "invalid",
                password: "invalid",
                password_confirmation: "lol"
            }
        end
        assert_template 'users/new'
    end

    test 'valid signup information' do
        get signup_path
        assert_difference 'User.count' do
            post_via_redirect users_path, user: {
                label: '12musterm',
                password: 'totallyvalid',
                password_confirmation: 'totallyvalid'
            }
        end
        assert_template 'users/show'
        assert_not_nil flash[:success]
    end
end
