require 'tk'

class RTD 

	def load_todos
		@todo_arr = IO.readlines("e:\\share\\todo.txt")
	end

	def print_todos
		@todo_arr.each { |e| print e }
	end

	def get_pri(pri)
		ret=[]
		@todo_arr.each do |td| 
			ret << td if td.start_with?("(#{pri})")
		end
		return ret
	end

	def init_tk
		@root = TkRoot.new { title "Ruby To Do"}
		@top_panes = TkPanedWindow.new(@root) do
			orient 'horizontal'
			pack 'fill' => 'both',
				  'expand' => 1
		end
		@bottom_panes = TkPanedWindow.new(@root) do
			orient 'horizontal'
			pack 'fill' => 'both',
				  'expand' => 1
		end
		@both_panes = TkPanedWindow.new(@root) do
			width 400
			height 800
			orient 'vertical'
			pack 'fill' => 'both',
				  'expand' => 1
		end
		@both_panes.add @top_panes
		@both_panes.add	@bottom_panes		  
	end

	def add_listbox(pri)
		lbox = scroll = nil
		lbox = TkListbox.new(@root) do
			width 0
			height 0
			pack 'fill' => 'both',
				  'expand' => 1
		end

		scroll = TkScrollbar.new(lbox) do
			pack 'fill' => 'y',
				 'side' => 'right'
			orient 'vertical'
  		end
  		lbox.yscrollbar(scroll)
		get_pri(pri).each do |td|
			lbox.insert 0, td
		end
		return lbox
	end

	def run
		load_todos
		init_tk
		@top_panes.add add_listbox("A")
		@top_panes.add add_listbox("B")
		@bottom_panes.add add_listbox("C")
		@bottom_panes.add add_listbox("D")
		print get_pri("A")
		#print_todos
		Tk.mainloop
	end
end

obj = RTD.new
obj.run
