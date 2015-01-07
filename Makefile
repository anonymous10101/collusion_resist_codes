con:
	python programs/gs_con.py
	
	gnuplot plots/plot_gs_ratio_con.gp
	mv ratio_group_con.txt plots/
	mv img_gs_ratio_con.eps images/
	
	gnuplot plots/plot_gs_perturb_con.gp
	mv perturb_group_con.txt plots/
	mv img_gs_perturb_con.eps images/
	
	python programs/tr_con.py
	
	gnuplot plots/plot_tr_loss_con.gp
	mv loss_truthful_con.txt plots/
	mv img_tr_loss_con.eps images/
	
	gnuplot plots/plot_tr_perturb_con.gp
	mv perturb_truthful_con.txt plots/
	mv img_tr_perturb_con.eps images/
	
dis:
	python programs/gs_dis.py
	
	gnuplot plots/plot_gs_ratio_dis.gp
	gnuplot plots/plot_up_ratio_dis.gp
	mv ratio_group_dis.txt plots/
	mv img_gs_ratio_dis.eps images/
	mv img_up_ratio_dis.eps images/
	
	gnuplot plots/plot_gs_perturb_dis.gp
	gnuplot plots/plot_up_perturb_dis.gp
	mv perturb_group_dis.txt plots/
	mv img_gs_perturb_dis.eps images/
	mv img_up_perturb_dis.eps images/
	
	python programs/tr_dis.py
	
	gnuplot plots/plot_tr_loss_dis.gp
	mv loss_truthful_dis.txt plots/
	mv img_tr_loss_dis.eps images/
	
	gnuplot plots/plot_tr_perturb_dis.gp
	mv perturb_truthful_dis.txt plots/
	mv img_tr_perturb_dis.eps images/

privacy:
	python programs/privacy.py
	
	gnuplot plots/plot_pk.gp
	mv img_pk.eps images/
	
	gnuplot plots/plot_tk.gp
	mv img_tk.eps images/
	mv privacy_dis.txt plots/
	