class AddIndexToUsersLabel < ActiveRecord::Migration
  def change
    add_index :users, :label, unique: true
  end
end
