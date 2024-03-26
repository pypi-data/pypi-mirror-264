from pathlib import Path
import math
import sys
import time
import os
import random
import glob
import pickle
import timeit

import numpy as np
import torch
from ase import Atoms

import aev
import rdb
try:
    import aevmod
except ModuleNotFoundError:
    pass

import hdf5_handler as hd

verbose  = False
diagnose = False
vverbose = False
testdb   = True
newhdfg  = True

home = Path.home()



# ====================================================================================================
def parse_meta_db(meta_db):
    nblk = len(meta_db)
    meta_parsed = []
    for blk in range(0, nblk):
        meta_parsed.append(parse_meta(meta_db[blk]))
        #print('in parse_meta_db: meta_parsed:',meta_parsed[0])
        #sys.exit('debug exit')
    return meta_parsed





def parse_meta(meta):
    meta_xyz = None
    meta_energy = None
    meta_method = None
    meta_type = None
    meta_name = None
    meta_path = None
    meta_force = None
    meta_name = None
    skip = 0
    if len(meta) == 1:
        lst = (" ".join(meta)).split(" ")
        for k, ent in enumerate(lst):
            if skip == 0:
                if ent == 'Energy':
                    meta_energy = lst[k + 1]
                    skip = 1
                elif ent == 'Method':
                    meta_method = lst[k + 1]
                    skip = 1
                elif ent == 'Type':
                    meta_type = lst[k + 1]
                    skip = 1
                elif ent == 'Name':
                    meta_name = lst[k + 1]
                    skip = 1
                elif ent == 'Path':
                    meta_path = lst[k + 1]
                    skip = 1
            # else:
            # sys.exit('parse_meta: Unknown keyword')
            else:
                skip = 0
    else:
        #print('building meta:')
        meta_energy = meta[-1]
        meta_force = meta[-2]
        meta_method = meta[2]
        try:
            meta_type = meta[3][0][1] + '_' + meta[3][1][1]
        except:
            meta_type = ''
        meta_xyz = [i[1] for i in meta[3] if i[0] == 'label'][0]
        meta_name = meta[1]
        #print("in parse_meta: meta:",meta)
        #print("in parse_meta: meta_energy:",meta_energy)
        #print("in parse_meta: meta_force:",meta_force)

    return meta_energy, meta_name, meta_method, meta_type, meta_name, meta_path, meta_xyz, meta_force




def sample_xid(meta_db, nsamp, npath=1, uniformdist=True):
    nblk = len(meta_db)
    if uniformdist:
        # extract unique names
        nm_uniq = np.unique(np.array([meta[1] for meta in meta_db]))
        # xyzid list of db for each name
        # Since the xyzid is unique within a given molecule configuration (e.g., CnHm),
        # the xyzid list store the molecule configuration and xyzid.
        rdxid = []
        for i in range(nm_uniq.shape[0]):
            list_nm = [[label[1].split('/') for label in meta[3] if label[0] == 'label'][0] for meta in meta_db if
                       meta[1] == nm_uniq[i]]
            if 'irc' in nm_uniq[i]:
                if len(list_nm) < npath:
                    print('for {} \nrequired points: {}\navailable points: {}'.format(nm_uniq[i], npath, len(list_nm)))
                    # sys.exit()
                else:
                    rdxid.extend(random.sample(list_nm, npath))
            else:
                if len(list_nm) < nsamp:
                    print('for {} \nrequired points: {}\navailable points: {}'.format(nm_uniq[i], npath, len(list_nm)))
                    # sys.exit()
                else:
                    rdxid.extend(random.sample(list_nm, nsamp))
        # sample random points from db for each name
    else:
        # sample random points from whole db
        if nblk < nsamp:
            print('required points: {}\navailable points: {}'.format(npath, nblk))
            # sys.exit()
        else:
            rdidx = random.sample(range(nblk), nsamp)
            try:
                rdxid = [[[label[1].split('/') for label in meta_db[i][3] if label[0] == 'label'][0]][0] for i in rdidx]
            except:
                rdxid = [meta_db[i][6].split('/') for i in rdidx]

    return rdxid

# ====================================================================================================

class Data_pes():
    """
	Data class relevant for PES construction and operations
	"""

    def __init__(self, atom_types=None):
        """
		Constructor for Data_pes class
		Defines atom_types and number of NNs
		"""
        if (atom_types):
            self.atom_types = atom_types
            self.num_nn = len(atom_types)

    def initialize(self, atom_types):
        self.atom_types = atom_types
        self.num_nn = len(atom_types)



    # ==============================================================================================
    def prep_aev(self, atom_types=['C', 'H'], nrho_rad=32, nrho_ang=8, nalpha=8, R_c=[4.6, 3.1]):

        # define list of atom types in system
        # atom_types = ['C', 'H']

        # set values for radial and angular symmetry function parameters
        # nrho_rad = 32  # number of radial shells in the radial AEV
        # nrho_ang = 8  # number of radial shells in the angular AEV
        # nalpha = 8  # number of angular wedges dividing [0,pi] in the angular AEV

        # instantiate AEV for given atom types, for given
        try:
            import aevmod
            myaev = aevmod.aev(atom_types, nrho_rad, nrho_ang, nalpha, R_c)
        except:
            myaev = aev.Aev(atom_types, nrho_rad, nrho_ang, nalpha, R_c)
            # set the dimension of the data vector being the input for each NN in the system
            self.dimdat = myaev.dout
            print("Constructed aev, output dimensionality is:", myaev.dout)

        # init data class with list of atom types in system
        self.initialize(atom_types)

        return myaev

    # ==============================================================================================
    def aev_from_xyz(self, xyz_db, nrho_rad=32, nrho_ang=8, nalpha=8, R_c=[4.6, 3.1], pack_n_write=True, myaev=None, nblk=None, meta_db=None):
        if myaev == None:

            # define list of atom types in system
            atom_types = ['C', 'H']

            # set values for radial and angular symmetry function parameters
            # nrho_rad = 32  # number of radial shells in the radial AEV
            # nrho_ang = 8  # number of radial shells in the angular AEV
            # nalpha = 8  # number of angular wedges dividing [0,pi] in the angular AEV

            # instantiate AEV for given atom types, for given
            try:
                import aevmod
                myaev = aevmod.aev(atom_types, nrho_rad, nrho_ang, nalpha, R_c)
            except:
                myaev = aev.Aev(atom_types, nrho_rad, nrho_ang, nalpha, R_c)
                # set the dimension of the data vector being the input for each NN in the system
                self.dimdat = myaev.dout
                print("Constructed aev, output dimensionality is:", myaev.dout)

            # init data class with list of atom types in system
            self.initialize(atom_types)

        else:
            atom_types = self.atom_types

        if nblk is None:
            nblk = len(xyz_db)
        if meta_db is None:
            parsed = [[0.0] for i in range(nblk)]
        else:
            parsed = parse_meta_db(meta_db)
        tag = None
        con = None

        # build daev database for available xyz database
        self.xyz_to_aev_db(xyz_db, nblk, parsed, myaev, tag, con, verbose=False, force=False)

        try:
            self.xyz_to_daev_db(xyz_db, nblk, myaev)
            # print('AEV derivatives were calculated.')
        except:
            pass
            #print('AEV derivatives were not calculated. Please check if aevmod is available.')

        return myaev

    # ==============================================================================================
    def aev_from_xyz_data(self, xyzfname, nrho_rad=32, nrho_ang=8, nalpha=8, R_c=[4.6,3.1], pack_n_write=True, myaev=None):
        #print('IN aev_from_xyz_data')
        if myaev == None:

            # define list of atom types in system
            atom_types = ['C', 'H']

            # set values for radial and angular symmetry function parameters
            # nrho_rad = 32  # number of radial shells in the radial AEV
            # nrho_ang = 8  # number of radial shells in the angular AEV
            # nalpha = 8  # number of angular wedges dividing [0,pi] in the angular AEV

            # instantiate AEV for given atom types, for given
            try:
                import aevmod
                myaev = aevmod.aev(atom_types, nrho_rad, nrho_ang, nalpha, R_c)
            except:
                myaev = aev.Aev(atom_types, nrho_rad, nrho_ang, nalpha, R_c)
                # set the dimension of the data vector being the input for each NN in the system
                self.dimdat = myaev.dout
                print("Constructed aev, output dimensionality is:", myaev.dout)

            # init data class with list of atom types in system
            self.initialize(atom_types)

        else:
            atom_types = self.atom_types

        print("parsing xyz data base (currently implements one input file only)")
        xyz_db, nblk, meta_db = db_parse_xyz(xyzfname)
        parsed = parse_meta_db(meta_db)
        tag = None  # tag = 'b3lyp/6-31G'
        con = None  # con = xyz_db[0][0]

        # build aev database for available xyz database
        print("Building PES AEV data base")
        self.xyz_to_aev_db(xyz_db, nblk, parsed, myaev, tag, con, verbose=False, force=False)
        #print('xyz_db: ', xyz_db)
        try:
            self.xyz_to_daev_db(xyz_db, nblk, myaev)
            # print('AEV derivatives were calculated.')
        except:
            print('AEV derivatives were not calculated. Please check if aevmod is available.')

        if pack_n_write:
            print("Packing data for writing aev_db_new.hdf5")
            hd.pack_data(verbose=False)

            print("Writing aev_db_new.hdf5")
            hd.write_aev_db_hdf("aev_db_new.hdf5")

        print("done...")
        print("ndat:", self.ndat)
        print("dimdat:", self.dimdat)

        return myaev


    def get_data(self, args, xid=None, fid=1, get_aevs=True):   #, testset=False):

        myaev = None



        # define list of atom types in system
        atom_types = args.present_elements

        # set values for radial and angular symmetry function parameters
        #nrho_rad = 32  # number of radial shells in the radial AEV
        #nrho_ang = 8  # number of radial shells in the angular AEV
        #nalpha = 8  # number of angular wedges dividing [0,pi] in the angular AEV

        nrho_rad = args.aev_params[0]  # number of radial shells in the radial AEV
        nrho_ang = args.aev_params[1]  # number of radial shells in the angular AEV
        nalpha = args.aev_params[2]    # number of angular wedges dividing [0,pi] in the angular AEV
        R_c = args.cuttoff_radius
        # instantiate AEV for given atom types, for given
        try:
            import aevmod
            myaev = aevmod.aev(atom_types, nrho_rad, nrho_ang, nalpha, R_c)
        except:
            myaev = aev.Aev(atom_types, nrho_rad, nrho_ang, nalpha, R_c)
            # set the dimension of the data vector being the input for each NN in the system
            self.dimdat = myaev.dout
            print("Constructed aev, output dimensionality is:", myaev.dout)

        # init data class with list of atom types in system
        self.initialize(atom_types)


        if args.input_data_type == 'sqlite':

            # read SQLite data base file 
            names = glob.glob(args.input_data_fname[0])
            print('names: ', names)
            print('len(names): ', len(names))
            if len(names) > 1:
                print("parsing multiple SQLite xyz databases")
                #if args.delta == True:
                xyz_db, nblk, meta_db = multiple_sqldb_parse_xyz(names, fid=fid, nameset=args.nameset,
                                                                 xid=xid, temp=args.temp, sort_ids=args.delta)
                print('SQLite xyz data was extracted, fid: {}'.format(args.fidlevel))
                if args.delta:
                    xyz_db_lf, nblk_lf, meta_db_lf = multiple_sqldb_parse_xyz(names, fid=args.fidlevel_lf, nameset=args.nameset,
                                                                              xid=xid, temp=args.temp, sort_ids=args.delta)
                    print('SQLite xyz data was extracted, fid: {}'.format(args.fidlevel_lf))
                    for i in range(len(meta_db)):
                        meta_db[i][-1] -= meta_db_lf[i][-1]
                        meta_db[i][-2] -= meta_db_lf[i][-2]

            else:
                #print('args.fidlevel: ', args.fidlevel)
                print("parsing SQLite xyz data base", args.input_data_fname[0])
                try:
                    if '/' in xid[0]:
                        xid_sep = [molid.split('/')[1] for molid in xid]
                    else:
                        xid_sep = xid
                except:
                    xid_sep = xid
                xyz_db, nblk, meta_db = sqldb_parse_xyz(args.input_data_fname[0], fid=fid,
                                                        nameset=args.nameset, xid=xid_sep, temp=args.temp, sort_ids=args.delta)
                if args.delta:
                    xyz_db_lf, nblk_lf, meta_db_lf = sqldb_parse_xyz(args.input_data_fname[0], fid=args.fidlevel_lf,
                                                        nameset=args.nameset, xid=xid_sep, temp=args.temp, sort_ids=args.delta)
                    if args.delta:
                        for i in range(len(meta_db[-1])):
                            meta_db[-1][i] -= meta_db_lf[-1][i]
                            meta_db[-2][i] -= meta_db_lf[-2][i]


            print('in get_data: nblk:', nblk)
            parsed = parse_meta_db(meta_db)
            #print('in get_data: got parsed[0]:',parsed[0])
            tag = None  # tag = 'b3lyp/6-31G'
            con = None  # con = xyz_db[0][0]
            force = args.wrf
            weights = args.wrw


        # build aev database for available xyz database
        print("Building PES AEV data base")
        del meta_db
        if get_aevs:
            self.xyz_to_aev_db(xyz_db, nblk, parsed, myaev, tag, con, force=force, weights=weights, verbose=False)
        else:
            self.get_xdat(xyz_db, nblk,  parsed, force=force)
        if force:
            try:
                print('Building derivative of AEV data base')
                self.xyz_to_daev_db(xyz_db, nblk, myaev)
            except:
                print('AEV derivatives were not calculated. Please check if aevmod is available.')


        print("done...")
        print("ndat:", self.ndat)
        #print("dimdat:", self.dimdat)


        return myaev

    def get_xdat(self, xyz_db, nblk, parsed, force):
        self.ndat=0
        full_energy_data = []
        if force:
            full_force_data = []
        self.full_symb_data = []
        self.pdat = []
        self.meta = []

        for blk in range(0, nblk):
            symb = xyz_db[blk][0]
            energy = parsed[blk][0]
            full_energy_data.append(energy)
            if force:
                full_force_data.append(parsed[blk][-1].flatten())   # HNN 7/31/22: changed from full_force_data.append(parsed[blk][-2].flatten())
            self.full_symb_data.append(symb)
            self.ndat = self.ndat + 1
            #self.pdat.append(np.reshape(x, (-1, 3)))
            self.meta.append(parsed[blk])

        self.xdat = np.empty([self.ndat, self.num_nn + 1], dtype=object)
        if force:
            self.fdat = np.empty([self.ndat, 1], dtype='float64').tolist()

        for i in range(0, self.ndat):
            xdatnn = [[]] * self.num_nn
            for j, s in enumerate(self.full_symb_data[i]):
                k = self.atom_types.index(s)
                xdatnn[k] = xdatnn[k] + []

            for k in range(0, self.num_nn):
                self.xdat[i][k] = xdatnn[k]

            #print('xyz_to_aev_db: i:',i,', num:',self.num_nn,',E:',full_energy_data[i])
            self.xdat[i][self.num_nn] = [float(full_energy_data[i])]
            if force:
                self.fdat[i] = [full_force_data[i]]
                #print('xyz_to_aev_db: Got force data')
        self.tvtmsk = np.ones([self.ndat], dtype=int)
        #self.ntrdat = self.ndat
        #self.nvldat = 0
        #self.ntsdat = 0


        #print('self.xdat: ', self.xdat)
        return


    # ==============================================================================================
    def get_data2(self, args, xid=None):   #, testset=False):

        myaev = None

        if args.input_data_type == 'aev':
            # read AEV data base hdf5 file
            print("Reading aev hdf5 data base (currently implements one input file only)")

            hd.read_aev_db_hdf(args.input_data_fname[0], args.ni, args.nf, verbose=False)
            hd.unpack_data(fdata=args.floss, verbose=False)

            print("done reading aev db ...")

        elif args.input_data_type == 'pca':

            # read AEV PCA data base hdf5 file
            print("Reading aev pca hdf5 data base (currently implements one input file only)")

            hd.read_pca_aev_db_hdf(args.input_data_fname[0], args.ni, args.nf, verbose=False)
            hd.unpack_data(verbose=False)

            print("done reading aev pca db ...")

        else:

            # define list of atom types in system
            atom_types = ['C', 'H']

            # set values for radial and angular symmetry function parameters
            #nrho_rad = 32  # number of radial shells in the radial AEV
            #nrho_ang = 8  # number of radial shells in the angular AEV
            #nalpha = 8  # number of angular wedges dividing [0,pi] in the angular AEV
            
            nrho_rad = args.aev_params[0]  # number of radial shells in the radial AEV
            nrho_ang = args.aev_params[1]  # number of radial shells in the angular AEV
            nalpha = args.aev_params[2]
            R_c = args.cuttoff_radius
            # instantiate AEV for given atom types, for given
            try:
                print('get_data trying')
                import aevmod
                myaev = aevmod.aev(atom_types, nrho_rad, nrho_ang, nalpha, R_c)
                print('Check!')
            except:
                print('Nope')
                myaev = aev.Aev(atom_types, nrho_rad, nrho_ang, nalpha, R_c)
                # set the dimension of the data vector being the input for each NN in the system
                self.dimdat = myaev.dout
                print("Constructed aev, output dimensionality is:", myaev.dout)

            # init data class with list of atom types in system
            self.initialize(atom_types)


            if args.input_data_type == 'sqlite':
                # during training set preparation, if xyzids for testset is specified,
                # read the xyzids, and exclude the xyzids when reading the sqlite db
                # if args.test_input_xid[0] is not None:
                #     f = open(args.test_input_xid[0], "r")
                #     with f:
                #         xyz = f.readlines()
                #
                #     xid = []
                #     for line in range(0, len(xyz)):
                #         lst = (" ".join(xyz[line].split())).split(" ")
                #         xid.append(lst[:2])
                #     f.close()
                #     if not testset:
                #         args.excludexid = True
                # else:
                #     xid = None

                # read SQLite data base file 
                print(args.input_data_fname)
                print(args.input_data_fname[0])
                names = glob.glob(args.input_data_fname[0])
                print('names: ', names)
                print('len(names): ', len(names))
                if len(names) > 1:
                #if '*' in args.input_data_fname[0]:
                    print("parsing multiple SQLite xyz databases")
                    xyz_db, nblk, meta_db = multiple_sqldb_parse_xyz(names, fid=args.fidlevel, nameset=args.nameset,
                                                                     xid=xid, temp=args.temp, sort_ids=args.delta)
                    print('SQLite xyz data was extracted, fid: {}'.format(args.fidlevel))

                else:
                    #print('args.fidlevel: ', args.fidlevel)
                    print("parsing SQLite xyz data base", args.input_data_fname[0])
                    try:
                        if '/' in xid[0]:
                            xid_sep = [molid.split('/')[1] for molid in xid]
                        else:
                            xid_sep = xid
                    except:
                        xid_sep = xid
                    xyz_db, nblk, meta_db = sqldb_parse_xyz(args.input_data_fname[0], fid=args.fidlevel,
                                                            nameset=args.nameset, xid=xid_sep, temp=args.temp, sort_ids=args.delta)
                
                #print('meta_db: ', meta_db)
                #print('xyz_db: ', xyz_db)
                print('in get_data: nblk:', nblk)
                #print('in get_data: got meta_db[0]:',meta_db[0])
                
                parsed = parse_meta_db(meta_db)
                
                #print('in get_data: got parsed[0]:',parsed[0])
                tag = None  # tag = 'b3lyp/6-31G'
                con = None  # con = xyz_db[0][0]
                force = args.wrf
                weights = args.wrw
            # else:
            # sys.exit("Unexpected input data type")

            # build aev database for available xyz database
            print("Building PES AEV data base")
            del meta_db
            self.xyz_to_aev_db(xyz_db, nblk, parsed, myaev, tag, con, force=force, weights=weights, verbose=False)

            if force:
                #self.xyz_to_daev_db(xyz_db, nblk, myaev)
                try:
                    print('Building derivative of AEV data base')
                    self.xyz_to_daev_db(xyz_db, nblk, myaev)
                except:
                    print('AEV derivatives were not calculated. Please check if aevmod is available.')

            # set the dimension of the data vector being the input for each NN in the system
            print("Constructed aev, output dimensionality is:", self.dimdat)

        print("done...")
        print("ndat:", self.ndat)
        print("dimdat:", self.dimdat)


        return myaev

    # ==========================================================================================

    

    def random_shuffle_aev_db(self):
        try:
            mapIndexPosition = list(zip(self.xdat, self.full_symb_data, self.pdat, self.meta, self.padded_fdat, self.w, self.fd2, self.fdat, self.padded_dxdat))
        except:
            try:
                mapIndexPosition = list(zip(self.xdat, self.full_symb_data, self.pdat, self.meta, self.padded_fdat, self.fd2, self.fdat, self.padded_dxdat))
                print('Shuffling without w')
            except:
                mapIndexPosition = list(zip(self.xdat, self.full_symb_data, self.pdat, self.meta))
                print('Shuffling without forces')
        random.shuffle(mapIndexPosition)
        try:
            self.xdat, self.full_symb_data, self.pdat, self.meta, self.padded_fdat, self.w, self.fd2, self.fdat, self.padded_dxdat = zip(*mapIndexPosition)
            print('random shuffle AEV, derivative of AEV, and weights')
        except:
            try:
                self.xdat, self.full_symb_data, self.pdat, self.meta, self.padded_fdat, self.fd2, self.fdat, self.padded_dxdat = zip(*mapIndexPosition)
                print('Did some Shufflin')
            except:
                print('No Forces shuffle')
                self.xdat, self.full_symb_data, self.pdat, self.meta = zip(*mapIndexPosition)
        #print('self.meta: ', self.meta)


    def write_aev_db_pickle(self, fname, myaev):
        d = {
            'laev': myaev.dout,
            'type': self.atom_types,
            'symb': self.full_symb_data,
            'xdat': self.xdat,
            'pdat': self.pdat,
            'meta': self.meta
        }
        # Pickle the 'data' dictionary using the highest protocol available.
        with open(fname, 'wb') as f:
            pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)

    def read_aev_db_pickle(self, fname, myaev):
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        with open(fname, 'rb') as f:
            d = pickle.load(f)
            assert (d['laev'] == myaev.dout)
            assert (checkEqual(d['type'], self.atom_types))
            self.full_symb_data = d['symb']
            self.xdat = d['xdat']
            self.pdat = d['pdat']
            self.meta = d['meta']

        self.ndat = len(self.xdat)
        self.tvtmsk = np.ones([self.ndat], dtype=int)
        self.ntrdat = self.ndat
        self.nvldat = 0
        self.ntsdat = 0

    def write_aev_db_txt(self, fname):
        """
		Method to save the AEV data base for the Data_pes object to a file
		"""
        print("write_aev_db_txt: writing file:", fname)

        with open(fname, 'w') as f:
            print(*self.atom_types, file=f)
            print(self.ndat, file=f)
            for i in range(self.ndat):
                print(len(self.xdat[i]), file=f)
                for x in self.xdat[i]:
                    print(len(x), file=f)
                    for ax in x:
                        if type(ax) is list:
                            print(len(ax), file=f)
                            print(*ax, file=f)
                        else:
                            print("1", file=f)
                            print(ax, file=f)
                print(*self.full_symb_data[i], file=f)
        return




    def xyz_to_daev_db(self, xyz_db, nblk, myaev):
        """
        Method to build the derivative of AEV data base for the Data_pes object
        """
        #print("xyz_to_aev_db", verbose)
        #del self.meta
        aevmodule = myaev.__class__.__module__
        #print('aev module:', aevmodule)

        if aevmodule != 'aevmod':
            print('No aevmod')
            print('aevmod module requires for Jacobian calculation')
            sys.exit()

        # J_C = []
        # J_H = []
        J_tot = []
        idx = [0]
        self.full_symb_data_daev = []
        for blk in range(0, nblk):
            if blk == 0:
                prev_symb = xyz_db[blk][0]
            symb = xyz_db[blk][0]
            self.full_symb_data_daev.append(symb)
            if prev_symb != symb:
                idx.append(blk)
                prev_symb = symb

        idx.append(nblk)
        for i in range(idx.__len__() - 1):
            symb = xyz_db[idx[i]][0]
            conf = aevmod.config(symb)
            for j in range(idx[i], idx[i + 1]):
                if j == idx[i]:
                    x = np.array([xyz_db[j][1].flatten()])
                else:
                    x_new = np.array([xyz_db[j][1].flatten()])
                    x = np.concatenate((x, x_new))

            npt = conf.add_structures(x)
            myaev.build_index_sets(conf)
            J = np.array(myaev.eval_Jac(conf))

            # idx_C = [a == 'C' for a in symb]
            for k in range(0, npt):
                J_tot.append(J[k])
                # tmp_C = []
                # tmp_H = []
                # for l in range(idx_C.__len__()):
                #     if idx_C[l]:
                #         tmp_C.append(J[k][l])
                #     else:
                #         tmp_H.append(J[k][l])
                # J_C.append(tmp_C)
                # J_H.append(tmp_H)

        # self.J_C = J_C
        # self.J_H = J_H

        self.ndat = nblk
        self.dxdat = np.empty([self.ndat, self.num_nn], dtype=object)

        for i in range(0, self.ndat):
            dxdatnn = [[]] * self.num_nn
            for j, s in enumerate(self.full_symb_data_daev[i]):
                k = self.atom_types.index(s)
                d = J_tot[i][j].tolist()
                #HHHHHHHHHHHHHHHHHHHHHHHHHHHH
                #if k==0:
                #    d.append(6.0)
                #elif k==1:
                #    d.append(1.0)
                #else:
                #    k.append(0.0)
                #HHHHHHHHHHHHHHHHHHHHHHHHHHHH
                
                dxdatnn[k] = dxdatnn[k] + [d]

            for k in range(0, self.num_nn):
                self.dxdat[i][k] = dxdatnn[k]
        
        #=====================================================
        d0 = len(self.dxdat)
        d1 = []
        d2 = []
        d3 = []
        d4 = []
        #print('padding dxdat')
        for i in range(len(self.dxdat)):
            d1.append(len(self.dxdat[i]))
            for j in range(len(self.dxdat[i])):
                d2.append(len(self.dxdat[i][j]))
                for k in range(len(self.dxdat[i][j])):
                    d3.append(len(self.dxdat[i][j][k]))
                    for v in range(len(self.dxdat[i][j][k])):
                        d4.append(len(self.dxdat[i][j][k][v]))

        
        #print('ARE WE THERE YET?')
        self.padded_dxdat = np.zeros((d0, max(d1), max(d2), max(d3), max(d4)))
        for i in range(len(self.dxdat)):
            for j in range(len(self.dxdat[i])):
                for k in range(len(self.dxdat[i][j])):
                    for v in range(len(self.dxdat[i][j][k])):
                        self.padded_dxdat[i][j][k][v][:len(self.dxdat[i][j][k][v])] = self.dxdat[i][j][k][v]
        
        d0 = len(self.fdat)
        d1 = []
        d2 = []
        print('padding fdat!')
        print(d0)
        for i in range(len(self.fdat)):
            d1.append(len(self.fdat[i]))
            for j in range(len(self.fdat[i])):
                d2.append(len(self.fdat[i][j]))
        self.fd2 = d2
        self.padded_fdat = np.zeros((d0, max(d1), max(d2)))
        for i in range(len(self.fdat)):
            for j in range(len(self.fdat[i])):
                self.padded_fdat[i][j][:len(self.fdat[i][j])] = self.fdat[i][j]
        del self.dxdat
        #=====================================================
        return

    def xyz_to_aev_db(self, xyz_db, nblk, parsed, myaev, target_theory=None, target_symb=None, force=True, weights=None, verbose=False):
        """
		Method to build the AEV data base for the Data_pes object
		"""
        #print("xyz_to_aev_db:", target_theory, target_symb, verbose)
        #print('IN xyz_to_aev_db')
        aevmodule = myaev.__class__.__module__
        #print('xyz_to_aev_db: aev module:', aevmodule)

        full_aev_data = []
        full_energy_data = []
        if force:
            full_force_data = []
        self.full_symb_data = []
        self.pdat = []
        self.meta = []

        self.ndat = 0
        for blk in range(0, nblk):
            if target_theory:
                if parsed[blk][2] != target_theory:
                    continue
            if target_symb:
                if not checkEqual(xyz_db[blk][0], target_symb):
                    continue

            energy = parsed[blk][0]   # HNN 7/31/22: changed from: parsed[blk][-1]
            #if blk == 0:
            #    print('xyz_to_aev_db: blk:',blk)
            #    print('xyz_to_aev_db: parsed:',parsed[blk])
            #    print('xyz_to_aev_db: energy:',energy)
            #sys.exit()

            if aevmodule == 'aevmod':
                symb = xyz_db[blk][0]
                conf = aevmod.config(symb)
                x = np.array([xyz_db[blk][1].flatten()])
                npt = conf.add_structures(x)
                myaev.build_index_sets(conf)
                y = np.array(myaev.eval(conf)[0])
            elif aevmodule == 'aev':
                conf = aev.Config(xyz_db[blk][0], xyz_db[blk][1])
                symb = conf.get_chemical_symbols()
                x = np.array([conf.get_positions().flatten()])

                if verbose:
                    print("blk:", format(blk, '04d'), "ndat:", format(self.ndat, '04d'), energy,
                          '%s' % ''.join(
                              [t + str(symb.count(t)) if symb.count(t) > 1 else t if symb.count(t) > 0 else '' for t in
                               myaev.types]))
                    if vverbose:
                        with np.printoptions(precision=4, suppress=True):
                            print("Configuration:", symb)
                            print("x:", [xp.tolist() for xp in np.reshape(x, (-1, 3))])

                conf.set_index_sets(*myaev.bld_index_sets(symb))
                y = myaev.eval(symb, *conf.get_index_sets(), x)[0]  # evaluate AEV

            full_aev_data.append(y)
            #print('full_aev_data: ', full_aev_data)
            full_energy_data.append(energy)
            if force:
                full_force_data.append(parsed[blk][-1].flatten())   # HNN 7/31/22: changed from full_force_data.append(parsed[blk][-2].flatten()) 
            self.full_symb_data.append(symb)
            self.ndat = self.ndat + 1
            self.pdat.append(np.reshape(x, (-1, 3)))
            self.meta.append(parsed[blk])

        #print('xyz_to_aev_db: full_energy_data[0]:',full_energy_data[0])
        #print('xyz_to_aev_db: parsed[0]:',parsed[0])
        #print('xyz_to_aev_db: full_force_data[0]:',full_force_data[0])

        self.dimdat = full_aev_data[0].shape[-1]


        # ==========================================================================================
        # prep data for training and testing

        # for i in range(0,ndat):
        #	print (i)
        #	print(full_aev_data[i],full_energy_data[i])

        # ==========================================================================================
        # Got ndat data points
        # each data point xdat[i] contains num_nn+1 objects, each of which is a list
        # xdat[i][0]        = [ [], [], ... [] ]   is a list of n0 lists
        #      n0 is the number of atoms of type 0 in the configuration
        #  and each inner list [] is the aev contents centered on the corresponding atom
        # xdat[i][1]        = [ [], [], ... [] ]   is a list of n1 lists
        #      n1 is the number of atoms of type 1 in the configuration
        #  and each inner list [] is the aev contents centered on the corresponding atom
        # ...
        # xdat[i][num_nn-1] = [ [], [], ... [] ]   is a list of n<num_nn-1> lists
        #      n<num_nn-1> is the number of atoms of type num_nn-1 in the configuration
        #  and each inner list [] is the aev contents centered on the corresponding atom
        # xdat[i][num_nn]   = []                   is a list containing 1 float
        #      this being the value of the energy for this data point
        #
        # tvtmsk[i] is a training-validation-testing mask, which will be defined as follows:
        # 	  1 if the data point will be part of the training   set    (default)
        #     0 if the data point will be part of the validation set (for hyper param optim)
        #    -1 if the data point will be part of the test       set
        # ntrdat is the number of training   points -- default ndat
        # nvldat is the number of validation points -- default 0
        # ntsdat is the number of test       points -- default 0
        # ==========================================================================================

        if weights == None:
            self.w = np.ones(self.ndat)
        else:
            if weights == 'z':
                nzone = 10
                zones = np.linspace(np.min(full_energy_data), np.max(full_energy_data), nzone)
                zones = zones[:-1]

                zid = np.digitize(full_energy_data, zones)
                zuniq, zcnts = np.unique(zid, return_counts=True)
                wt = 1 / zuniq.shape[0]

                self.w = np.empty(self.ndat)
                for i in range(0, self.ndat):
                    for j in range(zuniq.shape[0]):
                        if zid[i] == zuniq[j]:
                            self.w[i] = wt / zcnts[j]
            elif weights == 'c':
                names = []
                for i in range(self.ndat):
                    name = parsed[i][1]
                    names.append(name)
                # nuniq = list(set(names))
                # dicnm = dict(zip(nuniq, list(range(1, len(nuniq) + 1))))
                # zid = [dicnm[v] for v in names]
                zuniq, zcnts = np.unique(names, return_counts=True)
                wt = 1 / zuniq.shape[0]

                self.w = np.empty(self.ndat)
                for i in range(0, self.ndat):
                    for j in range(zuniq.shape[0]):
                        if names[i] == zuniq[j]:
                            self.w[i] = wt / zcnts[j]


        self.xdat = np.empty([self.ndat, self.num_nn + 1], dtype=object)
        if force:
            self.fdat = np.empty([self.ndat, 1], dtype='float64').tolist()

        for i in range(0, self.ndat):
            xdatnn = [[]] * self.num_nn
            for j, s in enumerate(self.full_symb_data[i]):
                k = self.atom_types.index(s)
                d = full_aev_data[i][j].tolist()
                #HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                #if k==0:
                #    d.append(6.0)
                #elif k==1:
                #    d.append(1.0)
                #else:
                #    k.append(0.0)
                #print(k,d)
                #HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
                xdatnn[k] = xdatnn[k] + [d]

            for k in range(0, self.num_nn):
                #print('xdatnn[k]: ', xdatnn[k])
                self.xdat[i][k] = xdatnn[k]

            #print('xyz_to_aev_db: i:',i,', num:',self.num_nn,',E:',full_energy_data[i])
            self.xdat[i][self.num_nn] = [float(full_energy_data[i])]
            if force:
                self.fdat[i] = [full_force_data[i]]
                #print('xyz_to_aev_db: Got force data')
        self.tvtmsk = np.ones([self.ndat], dtype=int)
        self.ntrdat = self.ndat
        self.nvldat = 0
        self.ntsdat = 0


        #print('self.xdat: ', self.xdat)
        return

    def set_tvt_mask2(self, tvtmsk=None, tvt=None):
        tst_ids = np.where(tvtmsk == '-1')[0]
        trv_ids = np.where(tvtmsk == '2')[0]

    def set_tvt_mask(self, tvtmsk=None, tvt=None):

        """
		Method to set masks defining the subsetting of the data into
		training, validation, and testing subsets
		tvtmsk[i] is ['molecule-name/xyzid', 'tag'], e.g.  ['C5H5/842314', '2'], with i=0,...,len(tvtmsk)-1
		where tag is:
		      -1 if the data point is for testing
		   and: 
		       2 .................... for training and validation
		   or: 
		       0 .................... for validation
		       1 .................... for training
        """

        #print(tvtmsk)
        #ltrvl = len([a[0] for a in tvtmsk if a[1] == '2'])
        #lts   = len([a[0] for a in tvtmsk if a[1] == '-1'])
        #lvl   = len([a[0] for a in tvtmsk if a[1] == '0'])
        #ltr   = len([a[0] for a in tvtmsk if a[1] == '1'])
        #print('in set_tvt_mask: tvtmsk[0]:',tvtmsk[0],', len:',len(tvtmsk),', tvt:',tvt)
        #print('ltrvl:',ltrvl)
        #print('lts  :',lts)
        #print('lvl  :',lvl)
        #print('ltr  :',ltr)
        

        

        if tvtmsk is not None and tvt is not None:
            if tvt[2] > 0:
                print('Error: Test set was set based on pre-set tvt mask file. The proportion of test set in the \'--tvt\' flag should be 0.')
                sys.exit()

        if tvtmsk is None:
            print('tvtmsk is None')
            assert (self.ntrdat >= 0 and self.nvldat >= 0 and self.ntsdat >= 0)
            assert (self.ntrdat + self.nvldat + self.ntsdat == self.ndat)

            # enforce the default
            self.tvtmsk = np.ones([self.ndat], dtype=int)

            nvt = self.nvldat + self.ntsdat
            if nvt == 0:
                return 0

            # generate nvt random *unique* integer samples in [0,ndat)
            # see: https://stackoverflow.com/questions/22842289/generate-n-unique-random-numbers-within-a-range
            if self.tvt_shuffle:
                ivt = random.sample(range(0, self.ndat), nvt)
                print('tvt mask was set randomly.')
            else:
                ivt = range(0, nvt)
            for i in ivt[0:self.nvldat]:
                self.tvtmsk[i] = 0

            for i in ivt[self.nvldat:nvt]:
                self.tvtmsk[i] = -1
            return 0
        else:
            #mla[i] is the 'molecule-name/xyzid' for data point i=0,..,ndat-1
            mla = np.array([m[-2] for m in self.meta])

            # enforce the default, 1->for training
            self.tvtmsk = np.ones([self.ndat], dtype=int)

            if tvt is None:
                tvt = [0.8, 0.2, 0.]
            if '2' in [a[1] for a in tvtmsk]:
                tvids = [a[0] for a in tvtmsk if a[1] == '2']
                print("tvids[0]:",tvids[0],' len:',len(tvids))
                #print(tvids)
                ntv = len(tvids)
            else:
                vlids = [a[0] for a in tvtmsk if a[1] == '0']
                print("vlids[0]:",vlids[0],' len:',len(vlids))
                trids = [a[0] for a in tvtmsk if a[1] == '1']
                print("trids[0]:",trids[0],' len:',len(trids))
                ntv = len(vlids) + len(trids)

            tstids = [a[0] for a in tvtmsk if a[1] == '-1']
            print("tstids[0]:",tstids[0],' len:',len(tstids))
            print("ntv:",ntv)

            # find and tag all the points in the dataset which are also tagged
            # in the tvt<>.txt input file as for testing
            for i in tstids:
                #ii = [idx for idx in range(self.ndat) if self.meta[idx][-2] == i][0]
                #self.tvtmsk[ii] = -1
                ii = np.where(mla == i)[0]
                if ii.size == 1:
                    self.tvtmsk[ii[0]] = -1
                elif ii.size > 1:
                    sys.exit('set_tvt_mask: found multiple matches in tstids')

            ntvt = sum(tvt)
            print('set_tvt_mask: ntvt,i.e. sum(tvt):',ntvt,', tvt:',tvt)

            if ntvt > 1:
                self.ntrdat = int(tvt[0])
                self.nvldat = int(tvt[1])
                self.ntsdat = len(tstids)
            else:
                self.ntrdat = int(tvt[0] * ntv)
                self.ntsdat = len(tstids)
                if ntvt == 1:
                    self.nvldat = self.ndat - self.ntrdat - self.ntsdat
                    if self.nvldat < 0:
                        print('data.py: set_tvt_mask: self.nvldat=',self.nvldat)
                        sys.exit('exiting in data.py')
                else:
                    self.nvldat = int(tvt[1] * ntv)
                    print('!!!WARNING!!! sum of tvt mask is not 1. You are using only partial dataset: {}%'.format(ntvt*100))

            print("self.ntrdat:",self.ntrdat)
            print("self.nvldat:",self.nvldat)
            print("self.ntsdat:",self.ntsdat)
            numtvt=self.ntrdat+self.nvldat+self.ntsdat
            print('numtvt:',numtvt,', self.ndat:',self.ndat)
            if numtvt > self.ndat:
                print('WARNING: based on specified tvt mask, numtvt > self.ndat')
                print('It will be over-ruled below just fyi')

            if self.nvldat > 0:
                if '2' in [a[1] for a in tvtmsk]:
                    if self.tvt_shuffle:
                        print(len(tvids), self.nvldat)
                        iv = random.sample(tvids, self.nvldat)
                        print('tvt mask for training/validation was set randomly.')
                    else:
                        iv = tvids[:self.nvldat]
                else:
                    iv = vlids

                if '/' not in self.meta[0][-2] and '/' in iv[0]:
                    iv = [i.split('/')[-1] for i in iv]

                # find and tag all the points in the dataset which are also tagged
                # in the tvt<>.txt input file as for validation
                for i in iv:
                    #ii = [idx for idx in range(self.ndat) if self.meta[idx][-2] == i][0]
                    #self.tvtmsk[ii] = 0
                    ii = np.where(mla == i)[0]
                    if ii.size == 1:
                        self.tvtmsk[ii[0]] = 0
                    elif ii.size > 1:
                        sys.exit('set_tvt_mask: found multiple matches in vlids')
            numts = len([i for i in range(0, self.ndat) if self.tvtmsk[i] == -1])
            numvl = len([i for i in range(0, self.ndat) if self.tvtmsk[i] ==  0])
            numtr = len([i for i in range(0, self.ndat) if self.tvtmsk[i] ==  1])
            numtv = len([i for i in range(0, self.ndat) if self.tvtmsk[i] ==  2])
            print('set_tvt_mask: final check on contents of self.tvtmsk')
            print('numts:',numts,', numvl:',numvl,', numtr:',numtr,', numtv:',numtv,', ndat:',self.ndat)
            if self.ntsdat != numts:
                sys.exit('mismatch in numts and self.ntsdat') 
            if self.nvldat != numvl:
                print(self.nvldat, numvl)
                sys.exit('mismatch in numvl and self.nvldat') 
            if self.ntrdat != numtr:
                print('mismatch in numtr and self.ntrdat') 

            print("self.ntrdat:",self.ntrdat)
            print("self.nvldat:",self.nvldat)
            print("self.ntsdat:",self.ntsdat)

            numtvt=self.ntrdat+self.nvldat+self.ntsdat
            print('numtvt:',numtvt,', self.ndat:',self.ndat)

            return 0

    def write_tvt_mask(self, fname):
        try:
            f = open(fname, "w")
        except IOError:
            print("write_tvt_mask: could not open file:", fname)
        # sys.exit()
        with f:
            print("write_tvt_mask: writing file: ... ", fname, end='')
            for i, msk in enumerate(self.tvtmsk):
                print('{:9d} {:3d}'.format(i, msk), file=f)
            print(" done")

    def prep_data(self, device='cpu'):
        """
		Method to prepare data by packaging it appropriately for NN batch computations
		"""
        self.irun = [i for i in range(0, self.ndat)]
        self.nat = [[self.full_symb_data[self.irun[i]].count(self.atom_types[t]) for i in range(len(self.irun))] for t in
                      range(self.num_nn)]
        self.nat_maxs = [max(i) for i in self.nat]
        
        self.aevs = [[[] for j in range(self.num_nn)] for i in range(len(self.irun))]
        for i in range(len(self.irun)):
            for j in range(self.num_nn):
                self.aevs[i][j] = torch.tensor(self.xdat[self.irun[i]][j])

        #print(self.dxdat)
        #try:
        self.daevs = [[[] for j in range(self.num_nn)] for i in range(len(self.irun))]
        for i in range(len(self.irun)):
            for j in range(self.num_nn):
                self.daevs[i][j] = torch.tensor([self.dxdat[self.irun[i]][j][k] for k in range(self.nat_maxs[j])])
        #except:
        #    pass
        if device != 'cpu':
            for i in range(len(self.irun)):
                for j in range(self.num_nn):
                    self.aevs[i][j] = self.aevs[i][j].to(device)
                    self.daevs[i][j] = self.daevs[i][j].to(device)

        return 0



    def prep_training_data(self, train_ind, bpath=None, with_aev_data=True):
        """
                Method to prepare training data by packaging it appropriately for NN batch computations
                """

        itr = [i for i in range(len(self.md)) if self.md[i] in train_ind]

        print('self.num_nn: ', self.num_nn)
        print('len(self.full_symb_data): ', len(self.full_symb_data))
        print('self.atom_types: ', self.atom_types)
        print('max(itr): ', max(itr))
        self.nattr = [[self.full_symb_data[itr[i]].count(self.atom_types[t]) for i in range(len(itr))] for t in
                      range(self.num_nn)]

        nattr_maxs = [max(i) for i in self.nattr]
        print('nattr_maxs: ', nattr_maxs)



        #names = np.array(self.meta)[:,1]
        #engs = np.array(self.meta)[:,0]
        #vn, cn = np.unique(names, return_counts=True)
        #name_dict = {}
        #for i in range(len(vn)):
        #    place = np.where(names == vn[i])[0]
        #    name_dict[vn[i]] = min(engs[place])


        self.train_aevs = [[[] for j in range(self.num_nn)] for i in range(len(itr))]
        self.train_engs = [[] for i in range(len(itr))]


        for i in range(len(itr)):
            if with_aev_data:
                for j in range(self.num_nn):
                    self.train_aevs[i][j] = torch.tensor(self.xdat[itr[i]][j])
            self.train_engs[i] = torch.tensor(self.xdat[itr[i]][-1])
        torch.save(self.train_engs, bpath+'train_engs')
        if with_aev_data:
            torch.save(self.train_aevs, bpath+'train_aevs')
            torch.save(self.dimdat, bpath+'aev_length')
        #del self.train_engs
        #del self.train_aevs

        try:
            self.train_daevs = [[[] for j in range(self.num_nn)] for i in range(len(itr))]
            self.train_forces = [[] for i in range(len(itr))]
            self.train_fdims = [[] for i in range(len(itr))]
            for i in range(len(itr)):
                if with_aev_data:
                    for j in range(self.num_nn):
                        self.train_daevs[i][j] = torch.tensor([self.padded_dxdat[itr[i]][j][k] for k in range(nattr_maxs[j])])
                self.train_forces[i] = torch.tensor([self.padded_fdat[itr[i]][0]])
                self.train_fdims[i] = len(self.fdat[itr[i]][0])
            if with_aev_data:
                torch.save(self.train_daevs, bpath+'train_daevs')
                del self.train_daevs
            torch.save(self.train_forces, bpath+'train_forces')
            torch.save(self.train_fdims, bpath+'train_fdims')
            #del self.train_daevs
            del self.train_forces
            del self.train_fdims
        except:
            pass

        return 0



    def prep_validation_data(self, bpath = None):
        """
		Method to prepare validation data by packaging it appropriately for NN batch computations
		"""
        print('data.py: prep_validation_data')

        ivl = [i for i in range(0, self.ndat) if self.tvtmsk[i] == 0]

        #print('ivl size:',len(ivl))
        #print('ndat:',self.ndat,', nvldat:',self.nvldat,', num_nn:',self.num_nn)

        self.natvl = [[self.full_symb_data[ivl[i]].count(self.atom_types[t]) for i in range(self.nvldat)] for t in
                      range(self.num_nn)]
        
        natvl_maxs = [max(i) for i in self.natvl]


        self.valid_aevs = [[[] for j in range(self.num_nn)] for i in range(len(ivl))]
        self.valid_engs = [[] for i in range(len(ivl))]

        for i in range(len(ivl)):
            for j in range(self.num_nn):
                self.valid_aevs[i][j] = torch.tensor(self.xdat[ivl[i]][j])
            self.valid_engs[i] = torch.tensor(self.xdat[ivl[i]][-1])
        torch.save(self.valid_engs, bpath+'valid_engs')
        torch.save(self.valid_aevs, bpath+'valid_aevs')

        try:
            self.valid_daevs = [[[] for j in range(self.num_nn)] for i in range(len(ivl))]
            self.valid_forces = [[] for i in range(len(ivl))]
            self.valid_fdims = [[] for i in range(len(ivl))]
            for i in range(len(ivl)):
                for j in range(self.num_nn):
                    self.valid_daevs[i][j] = torch.tensor([self.padded_dxdat[ivl[i]][j][k] for k in range(natvl_maxs[j])])
                self.valid_forces[i] = torch.tensor([self.padded_fdat[ivl[i]][0]])
                self.valid_fdims[i] = len(self.fdat[ivl[i]][0])
            torch.save(self.valid_daevs, bpath+'valid_daevs')
            torch.save(self.valid_forces, bpath+'valid_forces')
            torch.save(self.valid_fdims, bpath+'valid_fdims')
        except:
            pass


        return 0

    def prep_testing_data(self, test_ind, bpath=None, with_aev_data=True):
        """
                Method to prepare testing data by packaging it appropriately for NN batch computations
                """


        #tvtset = np.array(tvtmsk)[:,1]
        #tvtind = np.array(tvtmsk)[:,0]
        #test_spots = np.where(tvtset=='-1')[0]
        #tvtind = tvtind[test_spots]
        #these = set(tvtind)
        its = [i for i in range(len(self.md)) if self.md[i] in test_ind]

        #tvtmsk = np.array(tvtmsk)[:,1]
        #its = [i for i in range(0, self.ndat) if tvtmsk[i] == '-1']
        self.natts = [[self.full_symb_data[its[i]].count(self.atom_types[t]) for i in range(len(its))] for t in
                      range(self.num_nn)]

        natts_maxs = [max(i) for i in self.natts]


        self.test_aevs = [[[] for j in range(self.num_nn)] for i in range(len(its))]
        self.test_engs = [[] for i in range(len(its))]
        for i in range(len(its)):
            for j in range(self.num_nn):
                if with_aev_data:
                    self.test_aevs[i][j] = torch.tensor(self.xdat[its[i]][j])
            self.test_engs[i] = torch.tensor(self.xdat[its[i]][-1])
        torch.save(self.test_engs, bpath+'test_engs')
        if with_aev_data:
            torch.save(self.test_aevs, bpath+'test_aevs')
        try:
            self.test_daevs = [[[] for j in range(self.num_nn)] for i in range(len(its))]
            self.test_forces = [[] for i in range(len(its))]
            self.test_fdims = [[] for i in range(len(its))]
            for i in range(len(its)):
                if with_aev_data:
                    for j in range(self.num_nn):
                        self.test_daevs[i][j] = torch.tensor([self.padded_dxdat[its[i]][j][k] for k in range(natts_maxs[j])])
                self.test_forces[i] = torch.tensor([self.padded_fdat[its[i]][0]])
                self.test_fdims[i] = len(self.fdat[its[i]][0])
            if with_aev_data:
                torch.save(self.test_daevs, bpath+'test_daevs')
            torch.save(self.test_forces, bpath+'test_forces')
            torch.save(self.test_fdims, bpath+'test_fdims')
        except:
            pass

        return 0




# ====================================================================================================
# check that two lists match exactly
def checkEqual(L1, L2):
    return len(L1) == len(L2) and L1 == L2


# ====================================================================================================
def db_parse_xyz(name):
    """ Reads xyz database file and returns a list of lists, each of the latter containing two items:
		1) a list of strings, being chemical symbols of each atom in the configuration
		   e.g. ["H","H","O"] for a configuration with 2 H and 1 O atoms
		2) a 2d numpy array with n_atom rows and 3 columns, where
		   n_atom is the number of atoms in the configuration, and where
		   each row is the (x,y,z) coordinates of an atom in the configuration
		This is intended to be a means to read a file that's a concatenatenation of many xyz files
		each block can be a different configuration (e.g. different molecule) or the same config but in
		a different geometry
		If a config contains an atom not in the list of types, we stop later
	"""
    try:
        f = open(name, "r")
    except IOError:
        print("Could not open file:" + name)
    # sys.exit()
    with f:
        xyz = f.readlines()

    n_line = len(xyz)

    blk = 0
    line = 0
    while line < n_line:
        n_atom = int(xyz[line])
        meta = xyz[line + 1]
        symb = [" "] * n_atom
        x = np.zeros((n_atom, 3))
        l2 = line + 2
        for l in range(0, n_atom):
            lst = (" ".join(xyz[l + l2].split())).split(" ")
            symb[l] = lst[0]
            x[l] = np.array(lst[1:4])
        if blk == 0:
            xyz_db = [[symb, x]]
            meta_db = [[meta]]
        else:
            xyz_db.append([symb, x])
            meta_db.append([meta])

        # print("line:",line,", blk:",blk,sep="")
        # print("xyz_db[",blk,"][0]:",xyz_db[blk][0],sep="")
        # print("xyz_db[",blk,"][1]:",xyz_db[blk][1],sep="")

        line += n_atom + 2
        blk += 1

    return xyz_db, blk, meta_db


def sqldb_parse_xyz(name, fid=None, nameset=None, xid=None, ethsd=None, temp=None, posT=True, excludexid=False, sort_ids=True):
    """ Reads SQLite xyz database file and returns a list of lists, each of the latter containing two items:
		1) a list of strings, being chemical symbols of each atom in the configuration
		   e.g. ["H","H","O"] for a configuration with 2 H and 1 O atoms
		2) a 2d numpy array with n_atom rows and 3 columns, where
		   n_atom is the number of atoms in the configuration, and where
		   each row is the (x,y,z) coordinates of an atom in the configuration
		This is intended to be a means to read a file that's a concatenatenation of many xyz files
		each block can be a different configuration (e.g. different molecule) or the same config but in
		a different geometry
		If a config contains an atom not in the list of types, we stop later
	"""

    if posT:
        if temp != None:
            print('points at {} K will be loaded'.format(temp))
            posT = False
        else:
            temp = 0
            print('all points with positive temperature will be loaded')
    if nameset != None:
        print('Data is only from the db with the names: \n', nameset)
    if xid is not None:
        print('xyz id is preset')
        try:
            if '/' in xid[0]:
                xid = [x.split('/')[-1] for x in xid]
        except:
            pass

    config = name.split('/')[-1].split('.')[0]
    print('config: ', config)
    atom = Atoms(config)
    symb = atom.get_chemical_symbols()

    # t0 = timeit.default_timer()
    xyz_db = []
    meta_db = []
    idtest = []
    rdb.preamble()
    with rdb.create_connection(name) as conn:
        crsr = conn.cursor()
        if xid == None:
            if nameset == None:
                if ethsd == None:
                    if temp == None:
                        if fid == None:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id FROM xyz;'
                            record = crsr.execute(sql_query)  # execute the filtering
                        else:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id;'
                            record = crsr.execute(sql_query, str(fid))  # execute the filtering

                    else:
                        if posT:
                            if fid == None:
                                sql_query = f'SELECT xyz.geom, xyz.name, xyz.id FROM xyz WHERE xyz.temp>?;'
                                record = crsr.execute(sql_query, (str(temp),))  # execute the filtering
                            else:
                                sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.temp>? AND xyz.id=energy.xyz_id;'
                                record = crsr.execute(sql_query, (str(fid), temp))  # execute the filtering
                        else:
                            if fid == None:
                                sql_query = f'SELECT xyz.geom, xyz.name, xyz.id FROM xyz WHERE xyz.temp=?;'
                                record = crsr.execute(sql_query, (str(temp),))  # execute the filtering
                            else:
                                sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.temp=? AND xyz.id=energy.xyz_id;'
                                record = crsr.execute(sql_query, (str(fid), temp))  # execute the filtering
                else:
                    if temp == None:
                        sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND energy.E<?;'
                        record = crsr.execute(sql_query, (str(fid), ethsd))  # execute the filtering
                    else:
                        if posT:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND energy.E<? AND xyz.temp>?;'
                            record = crsr.execute(sql_query, (str(fid), ethsd, temp))  # execute the filtering
                        else:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND energy.E<? AND xyz.temp=?;'
                            record = crsr.execute(sql_query, (str(fid), ethsd, temp))  # execute the filtering
                for r in record:
                    xyz_db.append([symb, np.array(r['geom'])])
                    if fid == None:
                        meta_db.append([r['id'], r['name'], 0, np.array([['label', '{}/{}'.format(config, r['id'])]], dtype='<U12'), 0, 0])
                    else:
                        meta_db.append([r['id'], r['name'], r['calc'], r['calc_params'], r['Force'], r['E']])


            else:
                if ethsd == None:
                    if temp == None:
                        sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE xyz.name LIKE ? AND energy.fidelity=? AND xyz.id=energy.xyz_id;'
                        for nm in nameset:
                            record = crsr.execute(sql_query, (nm, str(fid)))  # execute the filtering
                            for r in record:
                                xyz_db.append([symb, np.array(r['geom'])])
                                meta_db.append([r['id'], r['name'], r['calc'], r['calc_params'], r['Force'], r['E']])
                                idtest.append(r['id'])
                    else:
                        if posT:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE xyz.name LIKE ? AND energy.fidelity=? AND xyz.temp>? AND xyz.id=energy.xyz_id;'
                        else:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE xyz.name LIKE ? AND energy.fidelity=? AND xyz.temp=? AND xyz.id=energy.xyz_id;'
                        for nm in nameset:
                            record = crsr.execute(sql_query, (nm, str(fid), temp))  # execute the filtering
                            for r in record:
                                xyz_db.append([symb, np.array(r['geom'])])
                                meta_db.append([r['id'], r['name'], r['calc'], r['calc_params'], r['Force'], r['E']])
                                idtest.append(r['id'])
                else:
                    if temp == None:
                        sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE xyz.name LIKE ? AND energy.fidelity=? AND energy.E<? AND xyz.id=energy.xyz_id;'
                        for nm in nameset:
                            record = crsr.execute(sql_query, (nm, str(fid), ethsd))  # execute the filtering
                            for r in record:
                                xyz_db.append([symb, np.array(r['geom'])])
                                meta_db.append([r['id'], r['name'], r['calc'], r['calc_params'], r['Force'], r['E']])
                                idtest.append(r['id'])
                    else:
                        if posT:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE xyz.name LIKE ? AND energy.fidelity=? AND energy.E<? AND xyz.temp>? AND xyz.id=energy.xyz_id;'
                        else:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE xyz.name LIKE ? AND energy.fidelity=? AND energy.E<? AND xyz.temp=? AND xyz.id=energy.xyz_id;'
                        for nm in nameset:
                            record = crsr.execute(sql_query, (nm, str(fid), ethsd, temp))  # execute the filtering
                            for r in record:
                                xyz_db.append([symb, np.array(r['geom'])])
                                meta_db.append([r['id'], r['name'], r['calc'], r['calc_params'], r['Force'], r['E']])
                                idtest.append(r['id'])

        else:
            if excludexid:
                if nameset == None:
                    if temp is None:
                        sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.id NOT IN (' + ','.join(
                            map(str, xid)) + ')'
                        record = crsr.execute(sql_query, str(fid))  # execute the filtering
                    else:
                        if posT:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.temp>? AND xyz.id NOT IN (' + ','.join(
                                map(str, xid)) + ')'
                        else:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.temp=? AND xyz.id NOT IN (' + ','.join(
                                map(str, xid)) + ')'
                        record = crsr.execute(sql_query, (str(fid), temp))  # execute the filtering
                    for r in record:
                        xyz_db.append([symb, np.array(r['geom'])])
                        meta_db.append([r['id'], r['name'], r['calc'], r['calc_params'], r['Force'], r['E']])
                        idtest.append(r['id'])
                else:
                    if temp == None:
                        sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE xyz.name LIKE ? AND energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.id NOT IN (' + ','.join(
                                    map(str, xid)) + ')'
                        for nm in nameset:
                            record = crsr.execute(sql_query, (nm, str(fid)))  # execute the filtering
                            for r in record:
                                xyz_db.append([symb, np.array(r['geom'])])
                                meta_db.append([r['id'], r['name'], r['calc'], r['calc_params'], r['Force'], r['E']])
                                idtest.append(r['id'])
                    else:
                        if posT:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE xyz.name LIKE ? AND energy.fidelity=? AND xyz.temp>? AND xyz.id=energy.xyz_id AND xyz.id NOT IN (' + ','.join(
                                    map(str, xid)) + ')'
                        else:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE xyz.name LIKE ? AND energy.fidelity=? AND xyz.temp=? AND xyz.id=energy.xyz_id AND xyz.id NOT IN (' + ','.join(
                                    map(str, xid)) + ')'
                        for nm in nameset:
                            record = crsr.execute(sql_query, (nm, str(fid), temp))  # execute the filtering
                            for r in record:
                                xyz_db.append([symb, np.array(r['geom'])])
                                meta_db.append([r['id'], r['name'], r['calc'], r['calc_params'], r['Force'], r['E']])
                                idtest.append(r['id'])

            else:
                if fid is not None:
                    if temp is None:
                        sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.id IN (' + ','.join(
                            map(str, xid)) + ')'
                        record = crsr.execute(sql_query, str(fid))  # execute the filtering
                    else:
                        if posT:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.temp>? AND xyz.id IN (' + ','.join(
                                map(str, xid)) + ')'
                        else:
                            #sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.temp=? AND xyz.id IN (' + ','.join(
                            #    map(str, xid)) + ')'
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id, energy.E, energy.calc, energy.calc_params, energy.Force FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.temp=? AND xyz.id IN (' + ','.join(
                                map(str, xid)) + ')'
                        record = crsr.execute(sql_query, (str(fid), temp))  # execute the filtering
                    for r in record:
                        xyz_db.append([symb, np.array(r['geom'])])
                        #meta_db.append([r['id'], r['name'], r['calc'], r['calc_params'], r['Force'], r['E']])
                        meta_db.append([r['id'], r['name'], 0, np.array([['label', '{}/{}'.format(config, r['id'])]], dtype='<U12'), r['Force'], r['E']])
                else:
                    if temp is None:
                        sql_query = f'SELECT xyz.geom, xyz.name, xyz.id FROM xyz WHERE xyz.id IN (' + ','.join(
                            map(str, xid)) + ')'
                        record = crsr.execute(sql_query)  # execute the filtering
                    else:
                        if posT:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id FROM xyz WHERE xyz.temp>? AND xyz.id IN (' + ','.join(
                                map(str, xid)) + ')'
                        else:
                            sql_query = f'SELECT xyz.geom, xyz.name, xyz.id FROM xyz WHERE xyz.temp=? AND xyz.id IN (' + ','.join(
                                map(str, xid)) + ')'
                        record = crsr.execute(sql_query, (temp,))  # execute the filtering
                    for r in record:
                        xyz_db.append([symb, np.array(r['geom'])])
                        meta_db.append(
                            [r['id'], r['name'], 0, np.array([['label', '{}/{}'.format(config, r['id'])]], dtype='<U12'), 0,
                             0])
    blk = len(xyz_db)
    print('sqldb_parse_xyz: nblk:', blk)

    if sort_ids:
        print('sorting by ids')
        ids = np.array([i[0] for i in meta_db])
        indx_sort = sorted(range(len(ids)), key=ids.__getitem__)
        xyz_db = [xyz_db[i] for i in indx_sort]
        meta_db = [meta_db[i] for i in indx_sort]#meta_db[indx_sort]
    

    return xyz_db, blk, meta_db




def write_tvtmsk_xyzid(dpes, dbname, sname=None, fidlevel=0, trxid=None, testxid=None, temp=0, nameset=None, uniformsamp=False):
    print('In write_tvtmsk_xyzid')
    if os.path.exists(sname):
        print('!!! Warning !!! \nyou already have the file: {} \nnew xyzid list will be appended to the existing file.'.format(sname))

    if fidlevel == None:
        print('fidelity level is not specified.')
        sys.exit()
    else:
        fidlevel = str(fidlevel)
    if isinstance(dbname, list):
        dbnames = dbname
    else:
        dbnames = [dbname]

    if testxid is None:
        ids_all = [dpes.meta[i][-2] for i in range(dpes.ndat)]
        for dbnm in dbnames:
            config = dbnm.split('/')[-1].split('.')[0]
            if not '/' in ids_all[0] and len(dbnames) > 1:
                print('molecule is not specified for a given xyzid list. please regenerate the hdf5 file using the updated script.')
                sys.exit()
            else:
                if '/' not in ids_all[0]:
                    ids = ids_all
                else:
                    ids = [molid.split('/')[1] for molid in ids_all if molid.split('/')[0] == config]
                idE_xyz = []
                rdb.preamble()
                with rdb.create_connection(dbnm) as conn:
                    crsr = conn.cursor()
                    if temp == 0:
                        sql_query = f'SELECT xyz.id, energy.E FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.id IN (' + ','.join(
                            map(str, ids)) + ')'
                        record = crsr.execute(sql_query, (fidlevel,))  # execute the filtering
                    else:
                        sql_query = f'SELECT xyz.id, energy.E FROM xyz, energy WHERE xyz.temp=? AND energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.id IN (' + ','.join(
                            map(str, ids)) + ')'
                        record = crsr.execute(sql_query, (temp, fidlevel))  # execute the filtering

                    for r in record:
                        idE_xyz.append(['{}/{}'.format(config, r['id']), r['E']])

                ids_sql = [id[0].split('/')[-1] for id in idE_xyz]
                if ids_sql != ids:
                    idE_xyz2 = []
                    if '/' in idE_xyz[0][0]:
                        for id in ids:
                            idE_xyz2.extend([idE for idE in idE_xyz if idE[0].split('/')[-1] == id])
                    else:
                        for id in ids:
                            idE_xyz2.extend([idE for idE in idE_xyz if idE[0] == id])
                    idE_xyz = idE_xyz2.copy()

                if '{}' in sname:
                    sname = sname.format(len(idE_xyz)) 
                f = open(sname, "a")
                #print('len dpes.ndata: ', len(dpes.ndata))
                #print('len dpes.tvtmsk: ', len(dpes.tvtmsk))
                #print('len idE_xyz: ', len(idE_xyz))
                write_2s=True
                with f:
                    print("write_tvt_mask: writing file: ... ", sname, end='')
                    if write_2s:
                        for i in range(0, len(idE_xyz)):
                            if dpes.tvtmsk[i] == -1:
                                print('{} {:3d} {:022.14e}'.format(idE_xyz[i][0], dpes.tvtmsk[i], idE_xyz[i][1]), file=f)
                            else:
                                print('{} {:3d} {:022.14e}'.format(idE_xyz[i][0], 2, idE_xyz[i][1]), file=f)
                    else:
                        for i in range(0, dpes.ndat):
                            print('{} {:3d} {:022.14e}'.format(idE_xyz[i][0], dpes.tvtmsk[i], idE_xyz[i][1]), file=f)
                    print(" done")

    else:
        print("write_tvt_mask: reading from sqlite db:",dbnames)
        for dbnm in dbnames:
            config = dbnm.split('/')[-1].split('.')[0]
            if not '/' in testxid[0] and len(dbnames) > 1:
                print('molecule is not specified for a given test xyzid list. please check the xyzid list file.')
                sys.exit()
            else:
                if '/' not in testxid[0]:
                    ids = testxid
                else:
                    ids = [molid.split('/')[1] for molid in testxid if molid.split('/')[0] == config]

            idE_tst = []
            rdb.preamble()
            with rdb.create_connection(dbnm) as conn:
                crsr = conn.cursor()
                if temp == 0:
                    sql_query = f'SELECT xyz.id, energy.E FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.id IN (' + ','.join(
                        map(str, ids)) + ')'
                    record = crsr.execute(sql_query, (fidlevel,))  # execute the filtering
                else:
                    sql_query = f'SELECT xyz.id, energy.E FROM xyz, energy WHERE xyz.temp=? AND energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.id IN (' + ','.join(
                        map(str, ids)) + ')'
                    record = crsr.execute(sql_query, (temp, fidlevel))  # execute the filtering

                for r in record:
                    idE_tst.append(['{}/{}'.format(config, r['id']), r['E']])

            idE_tr = []
            if trxid is None:
                # get unique name for entire dataset
                tmp = []
                if nameset is None:
                    rdb.preamble()
                    with rdb.create_connection(dbnm) as conn:
                        crsr = conn.cursor()
                        sql_query = f'SELECT xyz.name FROM xyz WHERE xyz.dist=0'
                        record = crsr.execute(sql_query)  # execute the filtering

                        for r in record:
                            tmp.append([r['name']])
                else:
                    for nm in nameset:
                        with rdb.create_connection(dbnm) as conn:
                            crsr = conn.cursor()
                            sql_query = f'SELECT xyz.name FROM xyz WHERE xyz.dist=0 AND xyz.name LIKE ?'
                            record = crsr.execute(sql_query, (nm,))  # execute the filtering
                            for r in record:
                                tmp.append([r['name']])

                uniqnms = np.unique(tmp)

                if uniformsamp:
                    nsamp = 100
                    npath = 20
                    print('{}: training points are selected randomly with nsamp={} and npath={}'.format(config, nsamp,
                                                                                                        npath))
                for nm in uniqnms:
                    # print('temp: {}, fidlevel: {}, nm: {}'.format(temp, fidlevel, nm))
                    if uniformsamp:
                        idE_tr_nm = []
                        rdb.preamble()
                        with rdb.create_connection(dbnm) as conn:
                            crsr = conn.cursor()
                            if temp == 0:
                                sql_query = f'SELECT xyz.name, xyz.id, energy.E FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.name=? AND xyz.id NOT IN (' + ','.join(
                                    map(str, ids)) + ') LIMIT ?'
                                if 'irc' in nm:
                                    record = crsr.execute(sql_query, (fidlevel, nm, npath))  # execute the filtering
                                else:
                                    record = crsr.execute(sql_query, (fidlevel, nm, nsamp))  # execute the filtering
                            else:
                                sql_query = f'SELECT xyz.name, xyz.id, energy.E FROM xyz, energy WHERE xyz.temp=? AND energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.name=? AND xyz.id NOT IN (' + ','.join(
                                    map(str, ids)) + ') LIMIT ?'
                                if 'irc' in nm:
                                    record = crsr.execute(sql_query, (temp, fidlevel, nm, npath))  # execute the filtering
                                else:
                                    record = crsr.execute(sql_query, (temp, fidlevel, nm, nsamp))  # execute the filtering
                            for r in record:
                                idE_tr_nm.append(['{}/{}'.format(config, r['id']), r['E']])
                            if 'irc' in nm:
                                if len(idE_tr_nm) < npath:
                                    print('!!! Warning !!! \nNot enough data points for {} in {}\nrequired points: {}\navailable points: {}'.format(nm, config, npath, len(idE_tr_nm)))
                                    sys.exit()
                                else:
                                    idE_tr.extend(idE_tr_nm)
                            else:
                                if len(idE_tr_nm) < nsamp:
                                    print('!!! Warning !!! \nNot enough data points for {} in {}\nrequired points: {}\navailable points: {}'.format(nm, config, nsamp, len(idE_tr_nm)))
                                    sys.exit()
                                else:
                                    idE_tr.extend(idE_tr_nm)
                    else:
                        rdb.preamble()
                        with rdb.create_connection(dbnm) as conn:
                            crsr = conn.cursor()
                            if temp == 0:
                                sql_query = f'SELECT xyz.name, xyz.id, energy.E FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.name=? AND xyz.id NOT IN (' + ','.join(
                                    map(str, ids)) + ')'
                                record = crsr.execute(sql_query, (fidlevel, nm))  # execute the filtering
                            else:
                                sql_query = f'SELECT xyz.name, xyz.id, energy.E FROM xyz, energy WHERE xyz.temp=? AND energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.name=? AND xyz.id NOT IN (' + ','.join(
                                    map(str, ids)) + ')'
                                record = crsr.execute(sql_query, (temp, fidlevel, nm))  # execute the filtering

                            for r in record:
                                idE_tr.append(['{}/{}'.format(config, r['id']), r['E']])


            else:
                if not '/' in trxid[0] and len(dbnames) > 1:
                    print(
                        'molecule is not specified for a given training xyzid list. please check the xyzid list file.')
                    sys.exit()
                else:
                    if '/' not in trxid[0]:
                        ids = trxid
                    else:
                        ids = [molid.split('/')[1] for molid in trxid if molid.split('/')[0] == config]

                rdb.preamble()
                with rdb.create_connection(dbnm) as conn:
                    crsr = conn.cursor()
                    if temp == 0:
                        sql_query = f'SELECT xyz.id, energy.E FROM xyz, energy WHERE energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.id IN (' + ','.join(
                            map(str, ids)) + ')'
                        record = crsr.execute(sql_query, fidlevel)  # execute the filtering
                    else:
                        sql_query = f'SELECT xyz.id, energy.E FROM xyz, energy WHERE xyz.temp=? AND energy.fidelity=? AND xyz.id=energy.xyz_id AND xyz.id IN (' + ','.join(
                            map(str, ids)) + ')'
                        record = crsr.execute(sql_query, (temp, fidlevel))  # execute the filtering
                    for r in record:
                        idE_tr.append(['{}/{}'.format(config, r['id']), r['E']])

            # print(len(idE_tr))
            if '{}' in sname:
                sname = sname.format(len(idE_tr))
            # print(sname)

            f = open(sname, "a")
            with f:
                print("write_tvt_mask: writing file: ... ", sname, end='')
                for i in range(0, idE_tr.__len__()):
                    print('{} {:3d} {:022.14e}'.format(idE_tr[i][0], 2, idE_tr[i][1]), file=f)
                for i in range(0, idE_tst.__len__()):
                    print('{} {:3d} {:022.14e}'.format(idE_tst[i][0], -1, idE_tst[i][1]), file=f)
                print(" done")
    return sname





# ====================================================================================================

# ====================================================================================================
def parse_xyz(name):
    """ Reads xyz file and returns a list containing two items:
		1) a list of strings, being chemical symbols of each atom in the system
		2) a 2d numpy array with n_atom rows and 3 columns where
		   each row is the (x,y,z) coordinates of an atom in the system
	"""
    try:
        f = open(name, "r")
    except IOError:
        print("Could not open file:" + name)
    # sys.exit()
    with f:
        xyz = f.readlines()

    n_line = len(xyz)
    n_atom = int(xyz[0])
    assert (n_line == n_atom + 2)

    symb = [" "] * n_atom
    x = np.zeros((n_atom, 3))

    for line in range(2, n_line):
        lst = (" ".join(xyz[line].split())).split(" ")
        symb[line - 2] = lst[0]
        x[line - 2] = np.array(lst[1:4])

    return symb, x


# ====================================================================================================
# ====================================================================================================
def read_xyz(name):
    """
	 Reads an xyz file using parse_xyz() and repackages the 2d array of
	 atom positions returned from it, converting it from a n_atom x 3 2d array
	 to a 1 x 3n_atom 2d array
	"""
    symb, x = parse_xyz(name)
    x = np.array([x.flatten()])

    return symb, x


# ====================================================================================================
def read_and_append_xyz(name, symb, x):
    symb_new, x_new = read_xyz(name)
    assert (checkEqual(symb, symb_new))
    x = np.concatenate((x, x_new))

    return symb, x


def read_and_append_xyz_torch(name, symb, x):
    symb_new, x_new = read_xyz(name)
    assert (checkEqual(symb, symb_new))
    x = np.concatenate((x, x_new))

    return symb, torch.tensor(x)


def append_xyz_torch(conf, symb, x):
    symb_new = conf.get_chemical_symbols()
    x_new = torch.tensor([conf.get_positions().flatten()])
    assert (checkEqual(symb, symb_new))
    x = np.concatenate((x, x_new))

    return symb, torch.tensor(x)


def append_xyz(conf, symb, x):
    symb_new = conf.get_chemical_symbols()
    x_new = np.array([conf.get_positions().flatten()])
    assert (checkEqual(symb, symb_new))
    x = np.concatenate((x, x_new))

    return symb, x


# ====================================================================================================
# ====================================================================================================



def multiple_sqldb_parse_xyz(names, fid=None, nameset=None, temp=None, xid=None, excludexid=False, posT=True, sort_ids=False):
    xyz_db = []
    nblk = 0
    meta_db = []
    meta_dist = []
    try:
        if '/' in xid[0]:
            xid_sep = [molid.split('/') for molid in xid]
        else:
            xid_sep = xid
    except:
        pass
    for name in names:
        if xid is not None:
            mol = name.split('/')[-1].split('.')[0]
            xidnew = [id[1] for id in xid_sep if id[0] == mol]
            xyz_db_temp, nblk_temp, meta_db_temp = sqldb_parse_xyz(name, fid=fid, nameset=nameset, temp=temp, xid=xidnew,
                                                                   excludexid=excludexid, posT=posT, sort_ids=sort_ids)
            #xyz_db_temp, nblk_temp, meta_db_temp, dist = sqldb_parse_xyz(name, fid=fid, nameset=nameset, temp=temp, xid=xidnew,
            #                                                       excludexid=excludexid, posT=posT)
        else:
            xyz_db_temp, nblk_temp, meta_db_temp = sqldb_parse_xyz(name, fid=fid, nameset=nameset, temp=temp, posT=posT, sort_ids=sort_ids)
            #xyz_db_temp, nblk_temp, meta_db_temp, dist = sqldb_parse_xyz(name, fid=fid, nameset=nameset, temp=temp, posT=posT)
        xyz_db.extend(xyz_db_temp)
        meta_db.extend(meta_db_temp)
        nblk = nblk + nblk_temp

    return xyz_db, nblk, meta_db


# ====================================================================================================

