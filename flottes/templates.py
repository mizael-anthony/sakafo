#-----------------------------------------------------
#----------- Flotte Templates ----------
#-----------------------------------------------------
class FlotteTemplate():
	index = 'flotte/flotte_list.html'
	list = 'flotte/includes/_flotte_list.html'
	create = 'flotte/includes/_flotte_create.html'
	update = 'flotte/includes/_flotte_update.html'
	virement = 'flotte/includes/_flotte_virement.html'

#-----------------------------------------------------
#---------------- Composante Templates ---------------
#-----------------------------------------------------
class ComposanteTemplate():
	# 1 - Composante Evaluation Formation
	detail_flotte_crud = 'composantes/detail_flotte/crud.html'
	detail_flotte_content = 'composantes/detail_flotte/content.html'

	# 2 - Composante Besoin Formation
	allocation_flotte_crud = 'composantes/allocation_flotte/crud.html'
	allocation_flotte_content = 'composantes/allocation_flotte/content.html'