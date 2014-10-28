class User < ActiveRecord::Base
    validates :label, presence: true, length: { is: 8 }, uniqueness: { case_sensitive: false }

    before_save { self.label = label.downcase }
end
