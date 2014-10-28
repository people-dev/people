class User < ActiveRecord::Base
    validates :label, presence: true, length: { maximum: 9 }, uniqueness: { case_sensitive: false }
    validates :password, presence: true, length: { minimum: 6 }

    before_save { self.label = label.downcase }

    has_secure_password
end
