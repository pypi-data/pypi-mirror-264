
if 'clise' in __file__:
	from clise.jsontool import cc
	import clise.tabletool as tt
	import clise.plottool as pt
else:
	from jsontool import cc
	import tabletool as tt
	import plottool as pt

from collections import OrderedDict

from astropy.io import fits
from astropy    import units as un
# from pint import UnitRegistry

import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.colors as colors
import scipy.optimize as opt
from scipy.interpolate import interp1d

# import matplotlib.cm as cm
import math

from scipy import ndimage
# from mpl_toolkits.axes_grid1 import make_axes_locatable
# from matplotlib import rc
# from matplotlib.patches import Circle

from IPython	import embed
import subprocess

from astropy.table import QTable

# un = UnitRegistry()
qu = un.Quantity
PSC = 206265  # plate scale convertor in arcsec

def mirror_formula(r0=31.697, z0=1005.805, l=87.86, xi=1.0):

	# Wolter-I formula
	a   = math.atan(r0 / z0) / 4.0
	tps = 2. * xi / (1. + xi) * a
	p   = z0 * math.tan(4. * a) * math.tan(tps)
	ths = 2. * (1. + 2. * xi) / (1. + xi ) * a
	d   = z0 * math.tan(4. * a) * math.tan(4. * a - ths)
	e   = math.cos(4. * a) * (1. + math.tan(4. * a) * math.tan(ths))

	p0 = 4 * e**2 * p * d / (e**2 - 1) + p**2
	p1 = p * 2

	h0 = e**2 * d**2
	h1 = e**2 * d * 2
	h2 = e**2 - 1

	print('p:', p0, p1)
	print('h:', h0, h1, h2)
	print('sanity check for IRT  ---------------------------------------------')
	z = z0 + l
	print('P end     ', z, math.sqrt(p1 * z + p0))
	z = z0
	print('inflection', z, math.sqrt(p1 * z + p0))
	z = z0
	print('inflection', z, math.sqrt(h2 * z**2 + h1 * z + h0))
	z = z0 - l
	print('H end     ', z, math.sqrt(h2 * z**2 + h1 * z + h0))
	print

	# convert Suzanne's
	Rp = p1 / 2
	Rh = h1 / 2 + h2 * z0
	Kh = -1 - h2

	r0p = math.sqrt(p1 * z0 + p0)
	r0h = math.sqrt(h2 * z0**2 + h1 * z0 + h0)
	print('sanity check for Suzanne ----------------------------------------------')
	print('ro:', r0p, r0h, r0p - r0h)
	print('Rp:', Rp, 'Kp:', 0.0)
	print('Rh:', Rh, 'Kh:', Kh)
	z = l
	print('P end     ', z, math.sqrt(2 * Rp * z + r0p**2))
	z = 0.0
	print('inflection', z, math.sqrt(2 * Rp * z + r0p**2))
	z = 0.0
	print('inflection', z, math.sqrt(2 * Rh * z - (Kh + 1) * z**2 + r0h**2))
	z = -l
	print('H end     ', z, math.sqrt(2 * Rh * z - (Kh + 1) * z**2 + r0h**2))

	# Ed's formula
	print('sanity check for Ed ----------------------------------------------')
	Rp = p1 / 2
	z0p = -p0 / p1

	z0h = (-h1 + math.sqrt(h1**2 - 4 * h2 * h0)) / 2 / h2
	Kh = -h2 - 1
	Rh = h2 * z0h + h1 / 2

	print('Rp:', Rp, 'Kp:', p1 * z0p + p0 - 1)
	print('Rh:', Rh, 'Kh:', Kh)
	res = h2 * z0p**2 + h1 * z0p + h0
	print('z0p:', z0p, 'z0h:', z0h, 'res:', res)

	z = z0 - z0p + l
	print('P end     ', z, math.sqrt(2 * Rp * z))
	z = z0 - z0p
	print('inflection', z, math.sqrt(2 * Rp * z))

	z = z0 - z0h
	print('inflection', z, math.sqrt(2 * Rh * z - (Kh + 1) * z**2))
	z = z0 - z0h - l
	print('H end     ', z, math.sqrt(2 * Rh * z - (Kh + 1) * z**2))
	print('z0p-z0h', z0p, z0h, z0p - z0h)

	print('    ', 2 * Rh / (Kh + 1))
	print
	# Rh = +0.7490674261976 - 1 + 0.001129
	# Kh = -0.0004964139768
	Kh = -h2 - 1
	Rh = h2 * z0p + h1 / 2
	print('sanity check')
	print('Rh:', Rh, 'Kh:', Kh, Rh + 1)
	z = z0 - z0p
	print('inflection', z, math.sqrt(2 * Rh * z - (Kh + 1) * z**2 + res))
	z = z0 - z0p - l
	print('H end     ', z, math.sqrt(2 * Rh * z - (Kh + 1) * z**2 + res))

def q2s(each, format=""):
	return f"{each.value:{format}} {str(each.unit).replace(' ','')}"

def plate_scale_raw(focal=1, pix=10):
	um2as = PSC / focal / 1000000
	print('plate scale for focal length:', focal, 'm', pix, 'um/pix')
	print('\t', um2as,	      'arcsec/um' )
	print('\t', 1. / um2as,	      'um/srcsec' )
	print('\t', pix * um2as,      'arcsec/pix')
	print('\t', 1. / um2as / pix, 'pix/srcsec')
	return um2as, pix * um2as

def plate_scale(focal='1m', pix=None, format=".4f"):
	"""calculate plate scale of the telescope
		-focal : focal length
		-pix   : pixel size
		-format: printing format
		e.g., -focal 1m -pix 10um
	"""

	focal = qu(focal)
	um2as = PSC * un.arcsec / focal.to(un.um)
	print('plate scale for focal length:', q2s(focal))
	for each in [um2as, 1. / um2as]: print("\t" + q2s(each, format))

	if pix is None: return um2as

	pix    = qu(pix + '/pix')
	pix2as = pix * um2as
	print('for pixel:', q2s(pix))
	for each in [pix2as, 1. / pix2as]: print("\t" + q2s(each, format))
	return um2as, pix2as

def twoD_Gaussian(coords, amplitude, x0, y0, sig_x, sig_y, theta, offset):
	x, y = coords

	a =  (np.cos(theta)**2 ) / (2 * sig_x**2) + (np.sin(theta)**2 ) / (2 * sig_y**2)
	b = -(np.sin(2 * theta)) / (4 * sig_x**2) + (np.sin(2 * theta)) / (4 * sig_y**2)
	c =  (np.sin(theta)**2 ) / (2 * sig_x**2) + (np.cos(theta)**2 ) / (2 * sig_y**2)

	g = offset + amplitude * \
		np.exp(-(a * ((x - x0)**2) + 2 * b * (x - x0) * (y - y0) + c * ((y - y0)**2)))

	return g.ravel()

def twoD_Gaussian_fit(data):
	# fits a 2D gaussian to the data and uses the fit to find the FWHM
	x, y       = np.meshgrid(*[np.arange(v) for v in data.shape])
	max_pixel  = np.unravel_index(np.argmax(data), data.shape)
	max_val    = data[max_pixel]
	guess      = [max_val, max_pixel[1], max_pixel[0], 5, 5, 0, 0]
	popt, pcov = opt.curve_fit(twoD_Gaussian, (x, y), data.ravel(), p0=guess)

	twoD_Gaussian((x, y), *popt).reshape(len(x), len(y))

	# fwhm_x = 2 * np.sqrt(2 * np.log(2)) * popt[3]
	# fwhm_y = 2 * np.sqrt(2 * np.log(2)) * popt[4]
	return popt

def multiples_to_single_image(img, options='mean'):
	# usually 10 images
	if   options == 'mean'  : img = np.mean(img, axis=0)
	elif options == 'sum'   : img = np.sum(img, axis=0)
	elif options == 'single': img = img[0, :, :]  # just use the first image
	elif options == 'roll'  :
		ishape = img.shape
		for idx in range(ishape[0]):
			img[idx, :, :] = np.roll(img[idx, :, :], -idx, axis=1)
		img = np.mean(img, axis=0)
	return img

def read_img(infile, hdu=0, filter=None, options=None):
	with fits.open(infile) as hdul:
		img = hdul[0].data

	img = multiples_to_single_image(img, options=options)

	if filter is not None:
		# x y swapped?
		img[filter[1]:filter[3], filter[0]:filter[2]] = 0
	return img

# ---------------------------------------------------------------------------
# Function to fit sum of sines
def sum_of_sines(x, *coeffs):
	n = len(coeffs) // 2
	return sum(coeffs[i] * np.sin(2 * np.pi * (i + 1) * x / 360 + coeffs[n + i]) for i in range(n))

# Fitting sine curve to remove decentering
def sine_model(x, a, b):
    return a * np.sin(np.radians(x) + b)
# ---------------------------------------------------------------------------
class xray_mirror:

	pix   = 1.35e-5   # in meters
	focal = 0.7		# in meters
	defocus = 0.0
	R_shell = 0.05	# 5 cm

	max_range = 300  	# max range in pixel
	plateau   = 150  	# plateau region
	center    = None  # peak location of the image or center of the image

	isImage   = None  #
	verbose   = 0

	# for event data
	x     = 'x_as'  	# x column
	y     = 'y_as'  	# x column
	bin   = 1		# bin size for radial distribution in pixels
	sigma = 0		# bin size for gaussian smoothing parameter

	# how to handle multiple images
	multiples = 'mean'

	# for bkgnd sub by matching outer section
	max_var     = 1.0
	max_iter    = 1000  	# maximum iterations
	start_ratio = 1.0		# starting ratio

	# image center search method and parameter
	# img_center_search = 'gaussian_fit'
	img_center_search = 'median'
	filter_sigma = 5.0

	# generic plotting options
	rcParams = OrderedDict()
	rcParams["figure.figsize"  ] = [6.8, 6]
	rcParams["figure.dpi"	   ] = 150
	rcParams["xtick.top"	   ] = False
	rcParams["ytick.right"	   ] = False
	rcParams["axes.grid"	   ] = False
	rcParams["xtick.direction" ] = "out"
	rcParams["ytick.direction" ] = "out"

	# annotate HPD, FWHM or center
	mark		= []
	calc_psf	= False
	color_hpd	= 'orange'
	color_fwhm	= 'yellow'
	alpha_hpd	= 0.8
	alpha_fwhm	= 0.8

	# plotting options
	zlog    = False
	zmin    = 0.0
	zmax    = None
	filter  = None
	flip_x  = swap   = False
	title   = ""
	x_med	  = y_med  = None
	xhist   = yhist  = None
	xslice  = yslice = None
	despine = None
	cmap    = 'gnuplot2_r'
	aspect  = 'equal'
	xlabel  = 'x offset in arcsec'
	ylabel  = 'y offset in arcsec'
	cb_off  = None

	do_radial = False
	aper    = 60.0

	# debugging options
	verbose = 1
	debug   = 0
	hold    = False

	# for reuse
	img    = None
	psf    = None
	radial = None

	def __init__(self, **kwpars):
		self.set_kwpars(kwpars)

	def set_kwpars(self, kwargs):
		ignored = []
		for key, val in kwargs.items():
			if hasattr(self, key): setattr(self, key, val)
			else:			     ignored.append(key)
			# if key == "img_center_search": print(key,val, self.img_center_search)
		if len(ignored) > 0:
			print(cc.err, 'Followings are not defined, so ignored, so double check:', cc.reset)
			print(cc.err, ignored, cc.reset)

		# automatic setting
		if self.yhist:
			if self.cb_off is None: self.cb_off = -0.18

		if self.zlog:
			if self.zmin <= 0: self.zmin = 1.e-3

		for each in ['HPD', 'FWHM']:
			if each in self.mark:
				self.calc_psf = True
				break

		if type(self.focal) is str:
			self.focal = qu(self.focal).to('m').value
		if type(self.pix) is str:
			self.pix = qu(self.pix).to('m').value
		if type(self.aper) is str:
			self.aper = qu(self.aper).to('arcsec').value
		if type(self.defocus) is str:
			self.defocus = qu(self.defocus).to('m').value
		if type(self.R_shell) is str:
			self.R_shell = qu(self.R_shell).to('m').value

		return 1

	def plate_scale(self, focal=None, pix=None):
		return plate_scale(str(self.focal) + 'm', str(self.pix) + 'm')

	def pix_to_arcsec(self, pixels):
		return 7200.0 * np.degrees(np.arctan(pixels * self.pix / (2 * self.focal)))

	def arcsec_to_pix(self, arcsec):
		return 2 * self.focal / self.pix * np.tan(np.radians(arcsec / 7200.0))

	def is_image(self, data):
		if type(data) is np.ndarray: self.isImage = True
		else:				     self.isImage = False

	def find_center(self, data, center=None):
		# it's given, just use it
		if center is None:
			self.center = center
			return

		if self.isImage:
			self.center = np.unravel_index(np.argmax(data), data.shape)
		else:
			self.center = [np.median(data[self.x]), np.median(data[self.y])]

	def find_center_event(self, data, center=None, x=None, y=None):
		# it's given, just use it
		if center is None:
			self.recenter = False
			return  center

		self.recenter = True
		return [np.median(data[x]), np.median(data[y])]

	def find_center_img(self, img, center=None, cornor=None, size=None):
		# it's given, just use it
		if center is not None:
			return center

		if self.img_center_search == 'gaussian_fit':
			# find max_pixel from gaussian fit if not specified
			# now only used for finding the centroid
			fit    = twoD_Gaussian_fit(img)
			center = [fit[1], fit[2]]

		elif self.img_center_search == 'peak':
			center = np.unravel_index(np.argmax(img), img.shape)

		elif self.img_center_search == 'median':
			medhigh = np.where(img > 0.5 * np.max(img))
			center  = np.median(medhigh[1]), np.median(medhigh[0])

		elif self.img_center_search == 'gaussian_filter':
			# if only one value is given, use gaussian_filter
			# this must be inherited from other program
			medimg = np.median(img)
			img_   = img - medimg
			img_[img_ < 0] = 0
			img_ = ndimage.gaussian_filter(img_, sigma=self.filter_sigma)

			center = np.unravel_index(np.argmax(img_), img_.shape)

		elif self.img_center_search == 'for_ring':
			# copied from image_fit.py
			# can't be more annoying about x & y
			cropped = img[cornor[1]:cornor[1]+size, cornor[0]:cornor[0]+size]

			lpa = np.sum(cropped, axis=0)
			lpb = np.sum(cropped, axis=1)
			la = np.round(np.median(np.where(lpa == np.max(lpa))[0]))
			lb = np.round(np.median(np.where(lpb == np.max(lpb))[0]))
			a, b = la + cornor[0], lb + cornor[1]
			center = [a, b]
			
			# plt.plot(lpa)
			# plt.plot(lpb)
			# plt.title('# 04')
			# plt.show()
			# pt.dplot(image=cropped)
			# pt.embed()

		if self.verbose >= 1: print(f"peak position from {self.img_center_search}: {center[0]:.1f} {center[1]:.1f} in pixels")
		return center

	def radial_distribution(self, data, center=None):
		if center is None: center = self.center

		if self.isImage:
			offset = np.arange(self.max_range).astype('float')
			radial = np.zeros_like(offset)
			x, y   = np.meshgrid(*[np.arange(v) for v in data.shape])
			r      = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)

			for i in np.arange(self.max_range): radial[i] = np.sum(data[r < i])
		else:
			bins   = int(self.max_range / self.bin)
			radial = np.zeros_like(np.arange(bins).astype('float'))

			data['offset'] = np.sqrt((data[self.x] - center[0])**2 + (data[self.y] - center[1])**2)
			offset = []
			total  = len(data.index)
			for i in np.arange(bins):
				radial[i] = data[data['offset'] < (self.bin * i)].count()['offset'] / total
				offset.append(self.bin * i)

		return radial, offset

	def bkgsub_by_mean(self, data):
		"""subtract the average value of the masked-out image
		"""
		# mask off focal spot to find & subtract mean of bg
		x, y = np.meshgrid(*[np.arange(v) for v in data.shape])
		r =  np.sqrt((x - self.center[1]) ** 2 + (y - self.center[0]) ** 2)
		masked = np.ma.masked_where(r < self.max_range, data)
		mean   = masked.mean()
		data  -= mean
		return data

	def bkgsub_by_match(self, src, bkg):
		"""iteratively subtract the background image by keeping the plateau region flat
		"""

		radial_src, _ = self.radial_distribution(src)
		radial_bkg, _ = self.radial_distribution(bkg)
		# ax_radial = np.arange(self.max_range - 1)

		# starting point of ratio is [0.9,1.1]
		itr = 0
		ratio = self.start_ratio
		# initial ratio is set to zero, then guess first
		if self.start_ratio == 0:
			x, y = np.meshgrid(*[np.arange(v) for v in src.shape])
			r =  np.sqrt((x - self.center[1]) ** 2 + (y - self.center[0]) ** 2)
			masked_src = np.ma.masked_where(r < self.max_range, src)
			masked_bkg = np.ma.masked_where(r < self.max_range, bkg)
			ratio = masked_src.mean() / masked_bkg.mean()

		# set the search range
		upper = 1.1 * ratio
		lower = 0.9 * ratio
		if self.debug == 2: pt.embed()
		# ann_src = radial_src[self.max_range - 1] - radial_src[self.plateau]
		# ann_bkg = radial_bkg[self.max_range - 1] - radial_bkg[self.plateau]

		# to ensure at least one iteration
		var_plateau = self.max_var + 1.0

		# now search the correct ratio to match the outer section of the images
		while abs(var_plateau) > self.max_var:
			radial = radial_src - ratio * radial_bkg
			dr = np.diff(radial)
			var_plateau = np.sum(dr[self.plateau:self.max_range - 1])
			itr += 1
			if itr >= self.max_iter: break
			if var_plateau < 0:
				upper = ratio
				ratio = 0.5 * (lower + ratio)
			else:
				lower = ratio
				ratio = 0.5 * (upper + ratio)

		if self.debug == 4: pt.embed()
		return radial, ratio, var_plateau, itr

	def find_HPD(self, radial, fraction=0.5):
		radial /= np.max(radial)  # sum of ALL cts
		hpd_pix = 2 * np.interp(fraction, radial, np.arange(radial.size))
		return self.pix_to_arcsec(hpd_pix)

	def find_ECF(self, radial, radius=30.0):
		radial /= np.max(radial)  # sum of ALL cts
		radius_pix = self.arcsec_to_pix(radius)
		ecf = np.interp(radius_pix, np.arange(radial.size), radial)
		return ecf

	def find_FWHM(self, data):
		"""
		Finds the FWHM in x and y directions using linear interpolation.
		This routine only works when the PSF shape is well defined peak with high statistics.
		"""

		center  = self.center
		max_val = data[center[1], center[0]]

		x       = data[center[0], :] / max_val
		x_left  = np.interp(0.5, x[:center[1]],	       np.arange(center[1])	         )
		x_right = np.interp(0.5, x[-1:center[1] - 1:-1], np.arange(len(x), center[1], -1))

		y       = data[:, center[1]] / max_val
		y_left  = np.interp(0.5, y[:center[0]],          np.arange(center[0])	         )
		y_right = np.interp(0.5, y[-1:center[0] - 1:-1], np.arange(len(y), center[0], -1))

		if self.verbose > 1: print(x_left, x_right, y_left, y_right)
		return self.pix_to_arcsec((x_right - x_left + y_right - y_left) / 2.)

	def find_FWHM2(self, data, recenter=True):
		"""
		Find the FWHM by finding the section above the half of the peak.
		This routine works more robustly even when the PSF shape is irregular
		slightly more prone to pixellation scale.
		"""

		if recenter: half_val = np.amax(data) * 0.5
		else:
			center   = [int(self.center[0]), int(self.center[1])]
			half_val = data[center[1], center[0]] * 0.5

		npix = np.count_nonzero(data >= half_val)

		fwhm_p = 2 * np.sqrt(float(npix) / math.pi)
		return self.pix_to_arcsec(fwhm_p)

	def find_FWHM3(self, data, max_pixel=None, recenter=True):
		"""
		Find the FWHM by finding the section above the half of the peak.
		This routine works more robustly even when the PSF shape is irregular
		get the widest FWHM possible.
		"""
		if recenter: half_val = np.amax(data) * 0.5
		else:
			center   = [int(self.center[0]), int(self.center[1])]
			half_val = data[center[1], center[0]] * 0.5

		indices = np.argwhere(data >= half_val)
		dx = np.max(indices[:, 0]) - np.amin(indices[:, 0])
		dy = np.max(indices[:, 1]) - np.amin(indices[:, 1])

		fwhm_p = np.sqrt(dx * dx + dy * dy)
		return self.pix_to_arcsec(fwhm_p)

	def calc_HPD_FWHM(self, radial, img=None):
		if not self.calc_psf: return None

		# find HPD and FWHM from gaussian fit
		psf = OrderedDict()

		psf['HPD']    = self.find_HPD(radial)
		psf['Aper']   = 60.0
		psf['HPDpix'] = self.arcsec_to_pix(psf['HPD'])

		psf['ECF_Aper'] = self.find_ECF(radial, radius=psf['Aper'] / 2.)
		psf['ECF_HPD']  = 0.5

		for each in self.mark:
			if each[-1] != "%": continue
			psf['ECF_' + each] = float(each[:-1]) * 0.01
			psf[each] = self.find_HPD(radial, fraction=psf['ECF_' + each])

		if img is not None:
			# find FWHM
			psf['FWHM_l'] = self.find_FWHM2(img)
			psf['FWHM_m'] = self.find_FWHM3(img)
			psf['FWHM'  ] = psf['FWHM_m'] if psf['FWHM_m'] > psf['FWHM_l'] else psf['FWHM_l']

			psf['ECF_FWHM'] = self.find_ECF(radial, radius=psf['FWHM'] / 2.0)

		if self.verbose >= 1:
			if img is not None:
				print(f"\tHPD = {psf['HPD']:0.1f}\" {psf['HPDpix']:0.1f}p, FWHM = {psf['FWHM_l']:0.1f} - {psf['FWHM_m']:0.1f}\"")
			else:
				print(f"\tHPD = {psf['HPD']:0.1f}\" {psf['HPDpix']:0.1f}p")
			print("\tECF = %0.1f" % (psf['ECF_Aper'] * 100.) + "% for 1' dia. aperture")

		return psf

	def clip_img(self, img, xr, yr, center=None):
		xr  = np.array(xr)
		yr  = np.array(yr)
		xpr = self.arcsec_to_pix(xr)
		ypr = self.arcsec_to_pix(yr)

		xii = int(center[0] + xpr[0])
		xfi = math.ceil(center[0] + xpr[1])

		yii = int(center[1] + ypr[0])
		yfi = math.ceil(center[1] + ypr[1])

		xr  = [self.pix_to_arcsec(xii - center[0] - 0.0), self.pix_to_arcsec(xfi - center[0] + 0.0)]
		yr  = [self.pix_to_arcsec(yii - center[1] - 0.0), self.pix_to_arcsec(yfi - center[1] + 0.0)]

		if self.verbose >= 3:
			print(xii, xfi, yii, yfi, xpr, ypr, center[0] - xpr[0], center[1] + xpr[1])

		# why is this so mixed up?
		clip = img[yii:yfi, xii:xfi]
		if self.hold: embed()
		clip[clip < 0] = 0

		ny  = len(img[0])
		nx  = len(img)
		ncy = len(clip[0])
		ncx = len(clip)

		if xii < 0:
			for ii in range(-xii):
				clip = np.r_[[np.zeros(ncy)], clip]
		if xfi >= nx:
			for ii in range(xfi - nx + 1):
				clip = np.r_[clip, [np.zeros(ncy)]]
		if yii < 0:
			for ii in range(-yii):
				clip = np.c_[np.zeros(ncx), clip]
		if yfi >= ny:
			for ii in range(yfi - yii + 1):
				clip = np.c_[clip, np.zeros(ncx)]

		return clip, [xii, xfi], [yii, yfi]

	def annotate_psf(self, plt, center, xr, yr, psf=None):
		if 'center' in self.mark:
			plt.plot(center[1], center[0], color='white', marker='+', markersize=2.0, alpha=0.8)

		if not self.calc_psf: return

		ax = plt.gca()
		tp = np.arange(1000) / 1000.
		if 'HPD' in self.mark:
			# likely focused images
			# alpha=0.3
			hpd = psf['HPD']
			xp  = hpd / 2 * np.cos(tp * math.pi * 2) + center[1]
			yp  = hpd / 2 * np.sin(tp * math.pi * 2) + center[0]
			plt.plot(xp, yp, color=self.color_hpd, linewidth=3, alpha=self.alpha_hpd)
			plt.xlim(xr)
			plt.ylim(yr)
			plt.text(0.95, 0.05, 'HPD: %.1f"' % hpd,
				transform=ax.transAxes, color=self.color_hpd, alpha=1.0, ha='right')

		if 'FWHM' in self.mark:
			fwhm = psf['FWHM']
			xp = fwhm / 2 * np.cos(tp * math.pi * 2) + center[1]
			yp = fwhm / 2 * np.sin(tp * math.pi * 2) + center[0]
			plt.plot(xp, yp, color=self.color_fwhm, linewidth=2, alpha=self.alpha_fwhm)
			plt.text(0.05, 0.05, 'FWHM: %.1f"' % fwhm,
				transform=ax.transAxes, color=self.color_fwhm, alpha=1.0, ha='left')

		if 'offset' in self.mark:
			offset = np.sqrt(center[0]**2 + center[1]**2) / 60.
			plt.text(0.05, 0.05, "Offset: %.1f'" % offset,
				transform=ax.transAxes, color=self.color_fwhm, alpha=1.0, ha='left')

	def plot_radial_distribution(self, radial, outfile=None, xscale='linear', psf=None, rdfile=None):
		if outfile is None: return

		rplot = pt.scatter()

		rcParams = OrderedDict()
		rcParams["legend.loc"]	= "center right"

		ax_radial_pix = np.arange(self.max_range)
		if xscale == 'linear':
			ax_radial = self.pix_to_arcsec(ax_radial_pix) / 60.0  # in arcmin
			xr = [-0.5, max(ax_radial)]
			xlabel = 'radius (arcmin)'
			arcsec_to_xaxis = 1. / 60.0
			xr2 = self.arcsec_to_pix(np.array(xr) / arcsec_to_xaxis)
		else:
			ax_radial = self.pix_to_arcsec(ax_radial_pix)  	# in arcsec
			xr = [1., max(ax_radial)]
			xlabel = 'radius (arcsec)'
			arcsec_to_xaxis = 1.0
			xr2 = self.arcsec_to_pix(np.array(xr) / arcsec_to_xaxis)

		if rdfile is not None:
			import pandas as pd
			col1 = pd.DataFrame({'radius': ax_radial})
			col2 = pd.DataFrame({'distribution': radial / max(radial)})
			dataFrame = pd.concat([col1, col2], axis=1)
			tt.to_csv_or_fits(rdfile, dataFrame, overwrite=True)

		yr = [-0.1, 1.1]
		# accumulative plot
		rplot.collect_data(xdata=ax_radial, ydata=radial / max(radial),
			label='accumulative', color="blue",
			marker='', linestyle='solid',
			rcParams=rcParams, bbox_to_anchor=[0.9, 0.55],
			add_ax2=True, xr2=xr2,
			title=self.title, grid=True, dolegend=False)

		# differential plot
		diff = np.diff(radial)
		rplot.collect_data(xdata=ax_radial[1:], ydata=diff / max(diff),
			marker='', linestyle='solid',
			label='differential', color="red")

		# plot
		ax, ax2, ay2 = rplot.mplot1d(xr=xr, xscale=xscale, yr=yr,
							ax2color='grey',
							xlabel=xlabel, ylabel='relative',
							xlabel2='radius (pixels)')
		ax.text(0.95, 0.95, 'accumulative', color='blue', ha='right', va='center', transform=ax.transAxes)
		ax.text(0.95, 0.05, 'differential', color='red',  ha='right', va='center', transform=ax.transAxes)

		color = 'orange'
		alpha = 0.5
		if psf is not None:

			text = OrderedDict()

			for each in self.mark:
				if each          not in psf: continue
				if 'ECF_' + each not in psf: continue
				y = psf['ECF_' + each]

				if   each     == "HPD": text[each] = '%-5s %5.1f"' % (each,  psf[each])
				elif each[-1] == "%"  : text[each] = '%-5s %5.1f"' % ('%i%%' % (y * 100), psf[each])
				else:                   text[each] = '%-5s %5.1f" %4.1f' % (each, psf[each], y * 100) + "%"

				radius = psf[each] / 2. * arcsec_to_xaxis
				ax.plot([xr[0],  radius], [y,     y], alpha=alpha, color=color)
				ax.plot([radius, radius], [yr[0], y], alpha=alpha, color=color)

			# for each in [self.max_range, self.plateau]:
			for each in [self.plateau]:
				radius = self.pix_to_arcsec(each) * arcsec_to_xaxis
				ax.plot([radius, radius], yr, alpha=alpha, color=color)

			if xscale == "log":
				for each in self.mark:
					if each          not in psf: continue
					if 'ECF_' + each not in psf: continue
					y = psf['ECF_' + each]
					ax.text(xr[0], y, " " + text[each], ha='left', va='center', family='monospace')

			else:
				ax.text(0.4, 0.5, "\n".join(text.values()), transform=ax.transAxes,
					ha='left', va='center', family='monospace')

			if self.debug == 5: pt.embed()

		plt.savefig(outfile)
		plt.clf()

	def get_psf_info_from_image(self, infile, outfile, xr, yr,
			bkgfile=None, fitsfile=None, radialplot=None, rdfile=None,
			hdu_src=0, hdu_bkg=0, reuse=False, center=None, wpix= None,
			**kwpars):

		# wpix is for having another axes but it doesn't work 
		# due to set_aspect error
		# axis being shared conflicts with alternative axis

		self.set_kwpars(kwpars)
		if self.verbose >= 2: print(infile)

		if reuse:
			if self.img is None:
				reuse = False

		if not reuse:
			self.center = center
			if self.verbose >= 3: print('reading the image')
			img = read_img(infile, hdu=hdu_src, options=self.multiples, filter=self.filter)
			self.is_image(img)

			# search the center of the image
			# from here: somehow merge with self.set_center above
			if self.verbose >= 3: print('finding the center')
			self.center = self.find_center_img(img, center=self.center)

			if self.debug == 1: pt.embed()
			# now bkgnd subtraction using radial distribution if bkgnd img given
			if bkgfile is not None:
				if self.verbose >= 2: print('with bkg')
				bkg = read_img(bkgfile, hdu=hdu_src, options=self.multiples, filter=self.filter)

				radial, ratio, var, itr = self.bkgsub_by_match(img, bkg)
				if self.verbose >= 3: print('iterations done', ratio, var, itr)
				if abs(var) > self.max_var: print('iterations failed:', var)

				img -= bkg * ratio

				# save processed data into new fits file
				if fitsfile is not None:
					hdu = fits.PrimaryHDU(img)
					hdu.writeto(fitsfile + '.fits.gz', overwrite=True)
			else:
				if self.verbose >= 2: print('no bkg')
				medimg = np.median(img)
				img   -= medimg
				if self.verbose >= 3: print('getting the radial distribution')
				# print(end='getting the radial distribution\n' if self.verbose >= 3 else '')
				radial, offset = self.radial_distribution(img)
				if self.verbose >= 3: print('bkg subtraction by the mean')
				img   = self.bkgsub_by_mean(img)

			if self.verbose >= 1:
				print(f"{self.title}:")
				print(f"\timage center = {self.center[0]:.1f}, {self.center[1]:.1f}")

			# save img, psf and reuse them?
			if self.verbose >= 3: print('calculating PSF if requested')
			self.psf    = self.calc_HPD_FWHM(radial, img)
			self.img    = img
			self.radial = radial

		# clip the image and plot the main 2-d image
		clip, xr2, yr2 = self.clip_img(self.img, xr, yr, center=self.center)

		if self.sigma > 0:
			import scipy.ndimage as ndimage
			clip = ndimage.gaussian_filter(clip, sigma=self.sigma)

		image, xedges, yedges = pt.dplot(image=clip / np.max(clip),
				xr=xr, yr=yr, title=self.title,
				xlabel=self.xlabel, ylabel=self.ylabel,
				cmap=self.cmap, zlog=self.zlog,
				zmin=self.zmin, zmax=self.zmax,
				xhist=self.xhist, yhist=self.yhist, despine=self.despine,
				xslice=self.xslice, yslice=self.yslice,
				cb_off=self.cb_off,
				aspect=self.aspect,
				# add_ax2=wpix is not None, 
				# add_ay2=wpix is not None, 
				# ax2color=wpix, ay2color=wpix,
				# xr2=xr2, yr2=yr2, 
				rcParams=self.rcParams, display=False, hold=self.hold)

		# annotate the image and save
		halfpix = self.pix_to_arcsec(0.5)
		self.annotate_psf(plt, [halfpix, halfpix], xr, yr, psf=self.psf)
		plt.savefig(outfile)
		plt.clf()

		# plot radial distribution
		if self.zlog:
			# self.plot_radial_distribution(radial, outfile=re.sub('.png$','_log.png',radialplot), xscale='log' ,    psf=psf)
			self.plot_radial_distribution(self.radial, outfile=radialplot, xscale='log' ,   psf=self.psf, rdfile=rdfile)
		else:
			self.plot_radial_distribution(self.radial, outfile=radialplot, xscale='linear', psf=self.psf, rdfile=rdfile)

	# this assumes the unit is in mm
	def get_psf_info_from_event(self, infile, outfile, xr, yr,
			x='X_mm', y='Y_mm',
			bkgfile=None, fitsfile=None, radialplot=None,
			hdu_src=0, hdu_bkg=0, **kwpars):

		self.set_kwpars(kwpars)
		if self.verbose >= 2: print(infile)

		self.pix = 1.e-3

		evt = tt.from_csv_or_fits(infile)
		self.isImage = False

		if self.flip_x:
			evt[x] = -evt[x]

		if self.swap:
			evt['y_as'] = self.pix_to_arcsec(evt[x])  # since each pix is 1 mm...
			evt['x_as'] = self.pix_to_arcsec(evt[y])
		else:
			evt['x_as'] = self.pix_to_arcsec(evt[x])
			evt['y_as'] = self.pix_to_arcsec(evt[y])

		self.center = self.find_center_event(evt, center=self.center, x='x_as', y='y_as')

		if self.verbose >= 1:
			print(f"{self.title}:")
			print(f"\timage center = {self.center[0]:.1f}, {self.center[1]:.1f}")

		# get HPD
		radial, offset = self.radial_distribution(evt)

		# now make 2d histogram
		xr = np.array(xr)
		yr = np.array(yr)

		xr = xr + self.center[0]
		yr = yr + self.center[1]

		# data cut within the window
		evt = evt.loc[evt['x_as'] >= xr[0]]
		evt = evt.loc[evt['x_as'] <= xr[1]]
		evt = evt.loc[evt['y_as'] >= yr[0]]
		evt = evt.loc[evt['y_as'] <= yr[1]]

		if self.recenter: self.center = self.find_center_event(evt, x='x_as', y='y_as')

		image, xedges, yedges = pt.dplot(xdata=evt['x_as'], ydata=evt['y_as'], binsize=self.bin,
				xr=xr, yr=yr, title=self.title,
				xlabel=self.xlabel, ylabel=self.ylabel,
				cmap=self.cmap, zlog=self.zlog, zmin=self.zmin,
				xhist=self.xhist, yhist=self.yhist, despine=self.despine,
				xslice=self.xslice, yslice=self.yslice,
				cb_off=self.cb_off,
				aspect=self.aspect,
				rcParams=self.rcParams, display=False, hold=self.hold)

		# npix = np.count_nonzero(image >= 0.5)
		psf  = self.calc_HPD_FWHM(radial, image)
		self.annotate_psf(plt, self.center, xr, yr, psf=psf)

		plt.savefig(outfile)
		plt.clf()
		plt.close("all")

	# ---------------------------------------------------------------------------
	# ring analysis

	def get_ring(self, img, radial=None, center=None, 
								extend_ring=250, cut_missing=0.15, avgover=1):

		from scipy.interpolate import CubicSpline
		from scipy.optimize import curve_fit
		from scipy.ndimage import rotate

		if center is None: 
			center=self.center

		if radial is None:
			radial, offset = self.radial_distribution(img, center=center)

		radial = radial/np.max(radial)
		r = np.min(np.where(radial > 0.95)[0])

		# Image rotation and HPD calculation
		a, b = center[1], center[0]
		r1 = r + extend_ring

		if a-r1 < 0: r1 = a
		if a+r1 > img.shape[0]: r1 = img.shape[0]-a
		if b-r1 < 0: r1 = b
		if b+r1 > img.shape[0]: r1 = img.shape[0]-b
		cropped = img[int(a-r1):int(a+r1), int(b-r1):int(b+r1)]

		x_size = len(cropped)//2
		x = np.arange(1, x_size + 1)
		# hpd = np.zeros((x_size, 360))

		from tqdm import tqdm

		# for i in tqdm(range(360), ascii=' '):
		R  = []
		xf = []
		hpd = []
		counts = []

		maximg = np.max(cropped)
		# for i in range(360):
		for i in tqdm(range(360), ascii=' '): #  
		# for i in tqdm(range(360), ascii=' ▖▘▝▗▚▞█'):
			# print(i)
			# pt.embed()
			ri = rotate(cropped, i, reshape=False)
			hpd_ = ri[len(ri)//2, len(ri)//2:]
			hpd_ = CubicSpline(x, hpd_, bc_type='natural')(x)
			R_   = np.where(hpd_ == np.max(hpd_))[0][0]
			# R[i] = np.mean(np.where(hpd[:, i] == np.max(hpd[:, i]))[0])
			# pt.embed()

			if hpd_[int(R_)]/maximg < 0.1: 
				   continue

			# print(i,R_, hpd_[int(R_)]/maximg)
			hpd.append(hpd_)
			R.append(R_)
			xf.append(i+1)
			counts.append(np.sum(hpd_))

		maxsig = np.max(counts)
		mask = counts > maxsig*cut_missing

		hpd    = np.array(hpd)
		hpd    = hpd.T
		xf     = np.array(xf)
		R      = np.array(R)
		counts = np.array(counts)

		hpd    = hpd[:, mask]
		xf     = xf[mask]
		R      = R[mask]
		counts = counts[mask]

		r_mean = np.mean(R)

		# need to redefine the center and repeat the work
		#
		# params, _ = curve_fit(sine_model, xf, R - r_mean)
		#
		# fitted_values = sine_model(xf, *params)
		# new_R = R - r_mean - fitted_values
		# pt.embed()
		#
		# # Refit if necessary
		# params, _ = curve_fit(sine_model, xf, new_R)
		# fitted_values = sine_model(xf, *params)
		# R_final = new_R - fitted_values
		#

		return xf, counts, R, r_mean, hpd, cropped

	def recenter_ring(self, xf, R, r_mean,  center=None):

		from scipy.optimize import curve_fit

		# need to redefine the center and repeat the work
		#
		params, _ = curve_fit(sine_model, xf, R - r_mean)

		fitted_values = sine_model(xf, *params)
		new_R = R - r_mean - fitted_values

		# Refit if necessary
		params2, _ = curve_fit(sine_model, xf, new_R)
		fitted_values2 = sine_model(xf, *params2)
		R_final = new_R - fitted_values2

		az = np.arange(1, 361)
		fitted_values = sine_model(az, *params)
		fitted_values2 = sine_model(az, *params2)

		dx = (r_mean + fitted_values + fitted_values2) * np.cos(np.radians(az)) 
		dy = (r_mean + fitted_values + fitted_values2) * np.sin(np.radians(az)) 

		return np.mean(dx), np.mean(dy)

	def get_ring_radius_resolution(self, xf, R, r_mean, hpd, cropped, center=None,
								extend_ring=250, cut_missing=0.15, avgover=1):

		from scipy.interpolate import CubicSpline
		from scipy.optimize import curve_fit
		from scipy.ndimage import rotate

		# Finding Axial HPDs
		ndata   = len(hpd[0])
		hpd_sorted= np.zeros(ndata)
		for i in range(hpd.shape[1]):
			cummilative = np.cumsum(np.sort(hpd[:, i])[::-1])
			f_half = cummilative[-1] / 2
			hpd_sorted[i] = np.sum(cummilative < f_half)
			# pt.embed()

		# Finding FWHM
		fwhmpix= np.zeros(len(hpd[0]))
		for i in range(hpd.shape[1]):
			max_val = np.max(hpd[:, i])
			fwhmpix[i] = np.sum(hpd[:, i] > max_val / 2)

		cs_r = CubicSpline(xf, R-r_mean, bc_type='natural')
		popt, _ = curve_fit(sum_of_sines, xf, cs_r(xf), p0=[1]*18)
		s = sum_of_sines(xf, *popt)
		# pt.embed()
		# plt.plot(xf, R-r_mean)
		# plt.plot(xf, s)
		# plt.show()

		# better HPD
		mode    = np.zeros(ndata)
		mean    = np.zeros(ndata)
		qc      = np.zeros(ndata)
		pixr    = np.arange(hpd.shape[0])
		hpd_nearpeak = np.zeros(ndata)
		hpd_central  = np.zeros(ndata)
		qt_nearpeak  = np.zeros((3,ndata))
		qt_central   = np.zeros((3,ndata))


		for i in range(hpd.shape[1]):
			current = hpd[:,i]
			for j in range(avgover):
				current = current + hpd[:, (i+j) % hpd.shape[1]]
				# this goes over the gap

			cumlat = np.cumsum(current)
			cumlat = cumlat / cumlat[-1]
			# qt_ = np.quantile(cumlat,[0.25,0.5,0.75])
			interpol = interp1d(cumlat, pixr)

			# mean[i] = np.sum(hpd[:,i]*pixr)/np.sum(hpd[:,i])
			mean[i] = np.sum(current*pixr)/np.sum(current)

			# more weight on high values
			peak = np.max(current)
			# hpd[hpd[:,i]<peak*0.5,i] = 0
			current[current<peak*0.5] = 0
			mode[i] = np.sum(current*pixr)/np.sum(current)
			# mode[i] = 3*qt_[1] - 2* mean[i]

			# qc_ = cumlat[int(s[i]+r_mean)]
			qc_ = cumlat[int(mode[i])]
			qc[i]=qc_
			low=qc_-0.25
			high=qc_+0.25
			if low  <= 0.01: low =0.01
			if high >= 0.99: high=0.99
			try:
				qt_ = interpol([low,qc_,high])
			except:
				pt.embed()
			hpd_nearpeak[i] = qt_[2]-qt_[0]
			qt_nearpeak[:,i] = qt_

			qt_= interpol([0.25,0.5,0.75])
			hpd_central[i] = qt_[2]-qt_[0]
			qt_central[:,i] = qt_

		# pt.embed()

		# mode =  3 median - 2 mean

		# plt.plot(xf, R-r_mean)
		# plt.plot(xf, s)
		# plt.plot(xf, qt[0,:]-r_mean)
		# plt.plot(xf, qt[1,:]-r_mean)
		# plt.plot(xf, qt[2,:]-r_mean)
		# plt.show()
		# plt.plot(xf, hpdpix)
		# plt.plot(xf, hpdpix2)
		# plt.show()

		# pt.dplot(image=cropped)
		# pt.embed()

		return s, hpd_sorted, hpd_nearpeak, hpd_central, \
				qt_nearpeak, qt_central, \
				fwhmpix, mean, mode, qc

	def get_ring_radius_resolution_(self, img, radial=None, center=None, 
								extend_ring=250, cut_missing=0.15, avgover=1):

		from scipy.interpolate import CubicSpline
		from scipy.optimize import curve_fit
		from scipy.ndimage import rotate

		if center is None: 
			center=self.center

		if radial is None:
			radial, offset = self.radial_distribution(img, center=center)

		radial = radial/np.max(radial)
		r = np.min(np.where(radial > 0.95)[0])

		# Image rotation and HPD calculation
		a, b = center[1], center[0]
		r1 = r + extend_ring

		if a-r1 < 0: r1 = a
		if a+r1 > img.shape[0]: r1 = img.shape[0]-a
		if b-r1 < 0: r1 = b
		if b+r1 > img.shape[0]: r1 = img.shape[0]-b
		cropped = img[int(a-r1):int(a+r1), int(b-r1):int(b+r1)]

		x_size = len(cropped)//2
		x = np.arange(1, x_size + 1)
		# hpd = np.zeros((x_size, 360))

		from tqdm import tqdm

		# for i in tqdm(range(360), ascii=' '):
		R  = []
		xf = []
		hpd = []
		counts = []

		maximg = np.max(cropped)
		# for i in range(360):
		for i in tqdm(range(360), ascii=' '): #  
		# for i in tqdm(range(360), ascii=' ▖▘▝▗▚▞█'):
			# print(i)
			# pt.embed()
			ri = rotate(cropped, i, reshape=False)
			hpd_ = ri[len(ri)//2, len(ri)//2:]
			hpd_ = CubicSpline(x, hpd_, bc_type='natural')(x)
			R_   = np.where(hpd_ == np.max(hpd_))[0][0]
			# R[i] = np.mean(np.where(hpd[:, i] == np.max(hpd[:, i]))[0])
			# pt.embed()

			if hpd_[int(R_)]/maximg < 0.1: 
				   continue

			# print(i,R_, hpd_[int(R_)]/maximg)
			hpd.append(hpd_)
			R.append(R_)
			xf.append(i+1)
			counts.append(np.sum(hpd_))

		maxsig = np.max(counts)
		mask = counts > maxsig*cut_missing

		hpd    = np.array(hpd)
		hpd    = hpd.T
		xf     = np.array(xf)
		R      = np.array(R)
		counts = np.array(counts)

		hpd    = hpd[:, mask]
		xf     = xf[mask]
		R      = R[mask]
		counts = counts[mask]

		r_mean = np.mean(R)

		# need to redefine the center and repeat the work
		#
		# params, _ = curve_fit(sine_model, xf, R - r_mean)
		#
		# fitted_values = sine_model(xf, *params)
		# new_R = R - r_mean - fitted_values
		# pt.embed()
		#
		# # Refit if necessary
		# params, _ = curve_fit(sine_model, xf, new_R)
		# fitted_values = sine_model(xf, *params)
		# R_final = new_R - fitted_values
		#

		# Finding Axial HPDs
		ndata   = len(hpd[0])
		hpd_sorted= np.zeros(ndata)
		for i in range(hpd.shape[1]):
			cummilative = np.cumsum(np.sort(hpd[:, i])[::-1])
			f_half = cummilative[-1] / 2
			hpd_sorted[i] = np.sum(cummilative < f_half)
			# pt.embed()

		# Finding FWHM
		fwhmpix= np.zeros(len(hpd[0]))
		for i in range(hpd.shape[1]):
			max_val = np.max(hpd[:, i])
			fwhmpix[i] = np.sum(hpd[:, i] > max_val / 2)

		# Function to fit sum of sines
		def sum_of_sines(x, *coeffs):
			n = len(coeffs) // 2
			return sum(coeffs[i] * np.sin(2 * np.pi * (i + 1) * x / 360 + coeffs[n + i]) \
				for i in range(n))

		cs_r = CubicSpline(xf, R-r_mean, bc_type='natural')
		popt, _ = curve_fit(sum_of_sines, xf, cs_r(xf), p0=[1]*18)
		s = sum_of_sines(xf, *popt)
		pt.embed()
		# plt.plot(xf, R-r_mean)
		# plt.plot(xf, s)
		# plt.show()

		# better HPD
		mode    = np.zeros(ndata)
		mean    = np.zeros(ndata)
		qc      = np.zeros(ndata)
		pixr    = np.arange(hpd.shape[0])
		hpd_nearpeak = np.zeros(ndata)
		hpd_central  = np.zeros(ndata)
		qt_nearpeak  = np.zeros((3,ndata))
		qt_central   = np.zeros((3,ndata))


		for i in range(hpd.shape[1]):
			current = hpd[:,i]
			for j in range(avgover):
				current = current + hpd[:, (i+j) % hpd.shape[1]]
				# this goes over the gap

			cumlat = np.cumsum(current)
			cumlat = cumlat / cumlat[-1]
			# qt_ = np.quantile(cumlat,[0.25,0.5,0.75])
			interpol = interp1d(cumlat, pixr)

			# mean[i] = np.sum(hpd[:,i]*pixr)/np.sum(hpd[:,i])
			mean[i] = np.sum(current*pixr)/np.sum(current)

			# more weight on high values
			peak = np.max(current)
			# hpd[hpd[:,i]<peak*0.5,i] = 0
			current[current<peak*0.5] = 0
			mode[i] = np.sum(current*pixr)/np.sum(current)
			# mode[i] = 3*qt_[1] - 2* mean[i]

			# qc_ = cumlat[int(s[i]+r_mean)]
			qc_ = cumlat[int(mode[i])]
			qc[i]=qc_
			low=qc_-0.25
			high=qc_+0.25
			if low  <= 0.01: low =0.01
			if high >= 0.99: high=0.99
			try:
				qt_ = interpol([low,qc_,high])
			except:
				pt.embed()
			hpd_nearpeak[i] = qt_[2]-qt_[0]
			qt_nearpeak[:,i] = qt_

			qt_= interpol([0.25,0.5,0.75])
			hpd_central[i] = qt_[2]-qt_[0]
			qt_central[:,i] = qt_

		# pt.embed()

		# mode =  3 median - 2 mean

		# plt.plot(xf, R-r_mean)
		# plt.plot(xf, s)
		# plt.plot(xf, qt[0,:]-r_mean)
		# plt.plot(xf, qt[1,:]-r_mean)
		# plt.plot(xf, qt[2,:]-r_mean)
		# plt.show()
		# plt.plot(xf, hpdpix)
		# plt.plot(xf, hpdpix2)
		# plt.show()

		# pt.dplot(image=cropped)
		# pt.embed()

		return xf, counts, R, s, r_mean, \
				hpd_sorted, hpd_nearpeak, hpd_central, \
				qt_nearpeak, qt_central, \
				fwhmpix, cropped, mean, mode, qc

	def get_ring_hpd_non_circularity(self, R_final, r_mean, 
								  defocus=0.012, R_shell=107.6071/2.0):
		# HPD from non-circularity
		f = self.focal * 1.0e3 # convert to mm from m
		R_fp = (R_final + r_mean) * self.pix * 1.0e3  # Convert to mm from m

		t = np.arctan((R_shell*1.0e3 - R_fp) / (f - defocus*1.0e3))
		fr = R_shell / np.tan(t)
		dx = np.tan(t) * (f - fr)

		alignment_defocus = np.mean(dx)
		sortddr = np.sort(np.abs(dx - alignment_defocus))

		# in arcsec?
		hpdddr = np.arctan(sortddr[len(sortddr) // 2] / self.focal) * 60 * 60

		return sortddr, hpdddr, dx

	def get_ring_info_from_image(self, infile, xr, yr, outfile=None,
			bkgfile=None, fitsfile=None, radialplot=None, rdfile=None, 
			plotlog=None, plotlin=None, plotprofile=None, title="",
			plotsorted=None, plotcentral=None,
			hdu_src=0, hdu_bkg=0, reuse=False, ratio=None,
			center=None, cornor=[750,1050], size=200, 
			extend_ring=200, 
			recenter_limit=1.0, max_iter=10,
			wpix= None, cut_missing=0.15, avgover=2,
			**kwpars):

		# wpix is for having another axes but it doesn't work 
		# due to set_aspect error
		# axis being shared conflicts with alternative axis

		if 'img_center_search' not in kwpars: kwpars['img_center_search'] = 'for_ring'
		self.set_kwpars(kwpars)
		if self.verbose >= 2: print(infile)

		if reuse:
			if self.img is None:
				reuse = False

		if not reuse:
			if self.verbose >= 3: print('reading the image')
			img = read_img(infile, hdu=hdu_src, options=self.multiples, filter=self.filter)
			self.is_image(img)

			# search the center of the image
			# from here: somehow merge with self.set_center above
			if self.verbose >= 3: print('finding the center')
			# self.img_center_search = 'for_ring'
			self.center = self.find_center_img(img, center=center, cornor=cornor, size=size)
			# print(self.center, center)

			if self.debug == 1: pt.embed()
			# now bkgnd subtraction using radial distribution if bkgnd img given
			if bkgfile is not None:
				if self.verbose >= 2: print('with bkg')
				bkg = read_img(bkgfile, hdu=hdu_src, options=self.multiples, filter=self.filter)

				if ratio is None:
					radial, ratio, var, itr = self.bkgsub_by_match(img, bkg)
					if self.verbose >= 3: 
						print('iterations done for bkgnd subtraction')
						print('\tratio: ', ratio)
						print('\tvar  : ', var)
						print('\titr  : ', itr)
					if abs(var) > self.max_var: print('iterations failed:', var)
				else: 
					radial = 0

				# if self.verbose >= 2: print('subtraction ratio:', ratio)
				# pt.embed()
				img -= bkg * ratio

				# repeat search for center after subtraction
				# perhaps needs an iteration
				self.center = self.find_center_img(img, center=center, cornor=cornor, size=size)
				# print(self.center, center)
				radial, offset = self.radial_distribution(img)

				# save processed data into new fits file
				if fitsfile is not None:
					hdu = fits.PrimaryHDU(img)
					hdu.writeto(fitsfile + '.fits.gz', overwrite=True)
			else:
				if self.verbose >= 2: print('no bkg')
				medimg = np.median(img)
				img   -= medimg
				if self.verbose >= 3: print('getting the radial distribution')
				# print(end='getting the radial distribution\n' if self.verbose >= 3 else '')
				radial, offset = self.radial_distribution(img)
				if self.verbose >= 3: print('bkg subtraction by the mean')
				img   = self.bkgsub_by_mean(img)

			if self.verbose >= 1:
				print(f"{self.title}:")
				print(f"\timage center = {self.center[0]:.1f}, {self.center[1]:.1f}")

			# save img, psf and reuse them?
			if self.verbose >= 3: print('calculating PSF if requested')
			# self.psf    = self.calc_HPD_FWHM(radial, img)

			# get the initial ring
			xf, counts, r, r_mean, hpd, cropped = self.get_ring(img, radial=radial,
														extend_ring=extend_ring, avgover=avgover,
														cut_missing=cut_missing)

			# reccenter it

			dx, dy = self.recenter_ring(xf, r, r_mean)

			print('recentering', dx, dy)
			self.center = [self.center[0] + dx *2, self.center[1] +dy*2]

			# get the ring again after recentering
			xf, counts, r, r_mean, hpd, cropped = self.get_ring(img, radial=radial,
														extend_ring=extend_ring, avgover=avgover,
														cut_missing=cut_missing)
			# for iter in range(max_iter):
			#
			# 	print(iter, 'recentering', dx, dy)
			# 	self.center = [self.center[0] + dx *1, self.center[1] +dy*1]
			#
			# 	# get the ring again after recentering
			# 	xf, counts, r, r_mean, hpd, cropped = self.get_ring(img, radial=radial,
			# 												extend_ring=extend_ring, avgover=avgover,
			# 												cut_missing=cut_missing)
			# 	dx, dy = self.recenter_ring(xf, r, r_mean)
			# 	if dx*dx+dy*dy <= recenter_limit: break


			s, hpd_sorted, hpd_nearpeak, hpd_central, \
				qt_nearpeak, qt_central, \
				fwhmpix, mean, mode, qc = self.get_ring_radius_resolution(xf, r, r_mean, hpd, cropped,
																extend_ring=extend_ring, avgover=avgover,
																cut_missing=cut_missing)

			sortddr, hpdddr, dx = self.get_ring_hpd_non_circularity(r, r_mean, 
											  defocus=self.defocus, R_shell=self.R_shell)

			self.img    = img
			self.radial = radial

			maxsig = np.max(counts)

			if outfile is None:
				# pt.plot1d(xdata=xdata, ydata=hpd           , display=True, title='hpd')
				pt.plot1d(xdata=xf, ydata=r             , display=True, title='Radius')
				pt.plot1d(xdata=xf, ydata=hpdpix        , display=True, title='Axial HPD')
				pt.plot1d(xdata=xf, ydata=fwhmpix       , display=True, title='Axial FWHM')
				pt.plot1d(xdata=xf, ydata=dx-np.mean(dx), display=True, title='Alignment Defocus')
				pt.plot1d(xdata=xf, ydata=sortddr       , display=True, title='Sorted DDR')
				pt.embed()

			else:
				print(outfile)
				table  = [xf, counts, r, s+r_mean, hpd_sorted, hpd_nearpeak, hpd_central, fwhmpix, dx, 
							qt_nearpeak[0,:], qt_nearpeak[1,:],qt_nearpeak[2,:],
							qt_central[0,:], qt_central[1,:],qt_central[2,:],
							qc,
				]
				names  = ["azimuth", "counts", "radius", "radius_sine", "hpd_sorted", "hpd_nearpeak", "hpd_central", "fwhmpix", "dx",
							"qt_nearpeak25", "qt_nearpeak50", "qt_nearpeak75",
							"qt_central25", "qt_central55", "qt_central75", "qc",
				]
				conv = self.pix_to_arcsec(1) * self.focal/(self.focal+self.defocus)

				str_hpd_nearpeak = '%5.1f"' % (np.sqrt(np.mean(hpd_nearpeak**2)) * conv)
				str_hpd_central  = '%5.1f"' % (np.sqrt(np.mean(hpd_central**2)) * conv)
				str_hpd_sorted   = '%5.1f"' % (np.sqrt(np.mean(hpd_sorted**2)) * conv)

				print('hpd_nearpeak %5.1f arcsec' % (np.sqrt(np.mean(hpd_nearpeak**2)) * conv))
				print('hpd_central  %5.1f arcsec' % (np.sqrt(np.mean(hpd_central**2)) * conv))
				print('hpd_sorted   %5.1f arcsec' % (np.sqrt(np.mean(hpd_sorted**2)) * conv))

				header = OrderedDict()
				header['R_MEAN'  ] = r_mean
				header['R_Shell' ] = self.R_shell
				header['focal'   ] = self.focal
				header['defocus' ] = self.defocus
				header['pix2as'  ] = self.pix_to_arcsec(1)
				header['as2pix'  ] = self.arcsec_to_pix(1)
				header['xo'      ] = self.center[0]
				header['yo'      ] = self.center[1]
				header['ratio'   ] = ratio
				header['hpdddr'  ] = hpdddr
				header['avgover' ] = avgover
				header['hpd_nrpk'] = np.sqrt(np.mean(hpd_nearpeak**2)) * conv
				header['hpd_cntl'] = np.sqrt(np.mean(hpd_central**2)) * conv
				header['hpd_srtd'] = np.sqrt(np.mean(hpd_sorted**2)) * conv

				data   = QTable(table, names=names, meta=header)
				data.write(outfile, overwrite=True,  format="fits")


			if plotprofile is not None:
				xf_=xf.copy()
				xf_[xf>180] = xf[xf>180]-360
				pt.plot1d(xdata=xf_,ydata=s+r_mean,color='red',linestyle='solid', 
						xtitle='azimuth', ytitle='ring in pix',
						display=False, title=title, 
						alpha=0.5, ymin=0.0, margin=0.05)
				print(plotprofile)
				plt.savefig(plotprofile)
				plt.clf()

			if plotlog is not None:
				isize=len(cropped[0,:])
				o = isize/2
				xr=[self.center[0]-o,self.center[0]+o]
				yr=[self.center[1]-o,self.center[1]+o]

				images, _, _ =pt.dplot(image=cropped, zlog=True, cmap='Blues',
						   xr=xr, yr=yr,  title=title+' HPW (nearpeak): '+str_hpd_nearpeak, 
						   zmin=1.0, aspect='equal', display=False)
				x = (s+r_mean) * np.cos(np.radians(xf))+o+xr[0]
				y = (s+r_mean) * np.sin(np.radians(xf))+o+yr[0]
				plt.plot(x,y,color='red',linestyle='solid', alpha=0.5)
				# x = qt[1,:] * np.cos(np.radians(xf))+o+xr[0]
				# y = qt[1,:] * np.sin(np.radians(xf))+o+yr[0]
				# plt.plot(x,y,color='orange',linestyle='solid', alpha=0.5)
				# x = mode * np.cos(np.radians(xf))+o+xr[0]
				# y = mode * np.sin(np.radians(xf))+o+yr[0]
				# plt.plot(x,y,color='green',linestyle='solid', alpha=0.5)
				# x = mean * np.cos(np.radians(xf))+o+xr[0]
				# y = mean * np.sin(np.radians(xf))+o+yr[0]
				# plt.plot(x,y,color='white',linestyle='solid', alpha=0.5)
				for idx, each in enumerate(xf):
					if idx % 5 != 0: continue
					if counts[idx] < maxsig*0.1: continue
					x = np.array([qt_nearpeak[0, idx],qt_nearpeak[2, idx]]) * np.cos(np.radians(each))+o+xr[0]
					y = np.array([qt_nearpeak[0, idx],qt_nearpeak[2, idx]]) * np.sin(np.radians(each))+o+yr[0]
					plt.plot(x,y,color='orange',linestyle='solid', alpha=0.5)

				plt.plot(self.center[0],self.center[1],marker='+',color='red', alpha=0.5)

				print(plotlog)
				plt.savefig(plotlog)
				plt.clf()

			if plotlin is not None:
				isize=len(cropped[0,:])
				o = isize/2
				xr=[self.center[0]-o,self.center[0]+o]
				yr=[self.center[1]-o,self.center[1]+o]

				images, _, _ =pt.dplot(image=cropped, zlog=False, cmap='Blues',
						   xr=xr, yr=yr,  title=title+' HPW (nearpeak): '+str_hpd_nearpeak, 
						   zmin=0.0, aspect='equal', display=False)
				x = (s+r_mean) * np.cos(np.radians(xf))+o+xr[0]
				y = (s+r_mean) * np.sin(np.radians(xf))+o+yr[0]
				plt.plot(x,y,color='red',linestyle='solid', alpha=0.5)
				for idx, each in enumerate(xf):
					if idx % 5 != 0: continue
					if counts[idx] < maxsig*0.1: continue
					x = np.array([qt_nearpeak[0, idx],qt_nearpeak[2, idx]]) * np.cos(np.radians(each))+o+xr[0]
					y = np.array([qt_nearpeak[0, idx],qt_nearpeak[2, idx]]) * np.sin(np.radians(each))+o+yr[0]
					plt.plot(x,y,color='orange',linestyle='solid', alpha=0.5)

				plt.plot(self.center[0],self.center[1],marker='+',color='red', alpha=0.5)
				print(plotlin)
				plt.savefig(plotlin)
				plt.clf()

			if plotsorted is not None:
				isize=len(cropped[0,:])
				o = isize/2
				xr=[self.center[0]-o,self.center[0]+o]
				yr=[self.center[1]-o,self.center[1]+o]

				images, _, _ =pt.dplot(image=cropped, zlog=True, cmap='Blues',
						   xr=xr, yr=yr,  title=title+' HPW (sorted): '+str_hpd_sorted, 
						   zmin=1.0, aspect='equal', display=False)
				x = (s+r_mean) * np.cos(np.radians(xf))+o+xr[0]
				y = (s+r_mean) * np.sin(np.radians(xf))+o+yr[0]
				plt.plot(x,y,color='red',linestyle='solid', alpha=0.5)
				for idx, each in enumerate(xf):
					if idx % 5 != 0: continue
					if counts[idx] < maxsig*0.1: continue
					sorted = [s[idx]+r_mean-hpd_sorted[idx]/2., s[idx]+r_mean+hpd_sorted[idx]/2.]
					x = np.array(sorted) * np.cos(np.radians(each))+o+xr[0]
					y = np.array(sorted) * np.sin(np.radians(each))+o+yr[0]
					plt.plot(x,y,color='orange',linestyle='solid', alpha=0.5)

				print(plotsorted)
				plt.plot(self.center[0],self.center[1],marker='+',color='red', alpha=0.5)
				plt.savefig(plotsorted)
				plt.clf()

			if plotcentral is not None:
				isize=len(cropped[0,:])
				o = isize/2
				xr=[self.center[0]-o,self.center[0]+o]
				yr=[self.center[1]-o,self.center[1]+o]

				images, _, _ =pt.dplot(image=cropped, zlog=True, cmap='Blues',
						   xr=xr, yr=yr,  title=title+' HPW (central): '+str_hpd_central, 
						   zmin=1.0, aspect='equal', display=False)
				x = (s+r_mean) * np.cos(np.radians(xf))+o+xr[0]
				y = (s+r_mean) * np.sin(np.radians(xf))+o+yr[0]
				plt.plot(x,y,color='red',linestyle='solid', alpha=0.5)
				for idx, each in enumerate(xf):
					if idx % 5 != 0: continue
					if counts[idx] < maxsig*0.1: continue
					x = np.array([qt_central[0, idx],qt_central[2, idx]]) * np.cos(np.radians(each))+o+xr[0]
					y = np.array([qt_central[0, idx],qt_central[2, idx]]) * np.sin(np.radians(each))+o+yr[0]
					plt.plot(x,y,color='orange',linestyle='solid', alpha=0.5)

				plt.plot(self.center[0],self.center[1],marker='+',color='red', alpha=0.5)
				print(plotcentral)
				plt.savefig(plotcentral)
				plt.clf()
		# # clip the image and plot the main 2-d image
		# clip, xr2, yr2 = self.clip_img(self.img, xr, yr, center=self.center)
		#
		# if self.sigma > 0:
		# 	import scipy.ndimage as ndimage
		# 	clip = ndimage.gaussian_filter(clip, sigma=self.sigma)
		#
		# image, xedges, yedges = pt.dplot(image=clip / np.max(clip),
		# 		xr=xr, yr=yr, title=self.title,
		# 		xlabel=self.xlabel, ylabel=self.ylabel,
		# 		cmap=self.cmap, zlog=self.zlog,
		# 		zmin=self.zmin, zmax=self.zmax,
		# 		xhist=self.xhist, yhist=self.yhist, despine=self.despine,
		# 		xslice=self.xslice, yslice=self.yslice,
		# 		cb_off=self.cb_off,
		# 		aspect=self.aspect,
		# 		# add_ax2=wpix is not None, 
		# 		# add_ay2=wpix is not None, 
		# 		# ax2color=wpix, ay2color=wpix,
		# 		# xr2=xr2, yr2=yr2, 
		# 		rcParams=self.rcParams, display=False, hold=self.hold)
		#
		# # annotate the image and save
		# halfpix = self.pix_to_arcsec(0.5)
		# self.annotate_psf(plt, [halfpix, halfpix], xr, yr, psf=self.psf)
		# plt.savefig(outfile)
		# plt.clf()
		#
		# # plot radial distribution
		# if self.zlog:
		# 	# self.plot_radial_distribution(radial, outfile=re.sub('.png$','_log.png',radialplot), xscale='log' ,    psf=psf)
		# 	self.plot_radial_distribution(self.radial, outfile=radialplot, xscale='log' ,   psf=self.psf, rdfile=rdfile)
		# else:
		# 	self.plot_radial_distribution(self.radial, outfile=radialplot, xscale='linear', psf=self.psf, rdfile=rdfile)

	def get_ring_gravity_vs_shell_panini(self, infile, roll=[0, 30.0], 
							   hold=False,
							   plotshell=None, plotradius=None, plotgravity=None, title="", **kwpars):

		# wpix is for having another axes but it doesn't work 
		# due to set_aspect error
		# axis being shared conflicts with alternative axis

		if 'img_center_search' not in kwpars: kwpars['img_center_search'] = 'for_ring'
		self.set_kwpars(kwpars)
		if self.verbose >= 2: print(infile)

		from scipy.interpolate import CubicSpline
		from scipy.optimize import curve_fit
		from scipy.fft import fft, ifft
		data=[]

		from os			  import path
		az = np.arange(1, 361)
		if plotradius is not None:
			pr = pt.scatter()
			pf = pt.scatter()
		for idx, eroll in enumerate(roll):
			data.append(OrderedDict())
			data[idx]['file'] = path.basename(infile[idx])
			data[idx]['dir' ] = path.dirname(infile[idx])
			data[idx]['roll'] = eroll
			radius, hdr = tt.from_csv_or_fits(infile[idx], withHeader=True)

			r_mean = float(hdr['R_MEAN' ])
			pix2as = float(hdr['PIX2AS' ])
			focal  = float(hdr['focal'  ])
			defocus= float(hdr['defocus'])

			x = radius["azimuth"]
			r = radius["radius_sine"] - r_mean
			r = r * pix2as * focal/(focal+defocus)

			data[idx]['x'] = x
			data[idx]['r'] = r
			# print(len(x),len(r))
			# pt.embed()

			cs_r = CubicSpline(x, r, bc_type='natural')
			popt, _ = curve_fit(sum_of_sines, az, cs_r(az), p0=[1]*18)
			s = sum_of_sines(az, *popt)
			s = np.array(s)

			data[idx]['cs_r'] = cs_r
			data[idx]['popt'] = cs_r

			if plotradius is not None:
				pr.collect_data(xdata=az, ydata=s, label=str(eroll)+'$^{\circ}$')
				pf.collect_data(xdata=az, ydata=np.roll(s, -eroll), label=str(eroll)+'$^{\circ}$')

			data[idx]['s'] = np.roll(s, -eroll)

		if plotradius is not None:
			pr.mplot1d(xlabel='azimuth (deg)', ylabel='offset from the mean radius', 
				display=False, margin=0.05, grid=True, title=title, **kwpars)
			plt.savefig(plotradius+'.png')
			plt.clf()
			pf.mplot1d(xlabel='azimuth (deg): aligned', ylabel='offset from the mean radius', 
				display=False, margin=0.05, grid=True, title=title, **kwpars)
			plt.savefig(plotradius+'_aligned.png')
			plt.clf()

			
		# pt.embed()
		# Remove gravity component btw 0, 1
		N = len(s)
		k = np.arange(1, N + 1)

		phase = data[0]['roll'] - data[1]['roll']
		index = N / phase * np.arange(1, phase + 1)
		index = index[index == np.floor(index)].astype(int)
		filter = np.ones(N)
		filter[index - 1] = 0
		b = filter * fft(data[0]['s'] - data[1]['s']) / (1 - np.exp(-1j * 2 * np.pi * phase * k / N))
		if hold: pt.embed()
		data[0]['shell'] = ifft(b).real
		data[1]['shell'] = ifft(b).real
		data[0]['gravity'] = data[0]['s'] - data[0]['shell']
		data[1]['gravity'] = data[1]['s'] - data[1]['shell']

		data[0]['rms_shell'  ] = np.sqrt(np.mean(data[0]['shell'  ]**2))
		data[1]['rms_shell'  ] = np.sqrt(np.mean(data[1]['shell'  ]**2))
		data[0]['rms_gravity'] = np.sqrt(np.mean(data[0]['gravity']**2))
		data[1]['rms_gravity'] = np.sqrt(np.mean(data[1]['gravity']**2))

		print("roll      shell instrinsic       gravity")
		for each in data:
			print("%3d deg" % each['roll'], "%7.2f arcsec" % each['rms_shell'], 
					"%10.2f arcsec" % each['rms_gravity'], 
					each['file'], each['dir'])

		if plotgravity is not None:
			# x = (60.0) * np.cos(np.radians(az))
			# y = (60.0) * np.sin(np.radians(az))
			# plt.plot(x,y,color='grey',linestyle='solid', alpha=0.5)
			# plt.title('gravit mount effects + 60 arcsec')
			# x = (data[0]['gravity']+60.0) * np.cos(np.radians(az))
			# y = (data[0]['gravity']+60.0) * np.sin(np.radians(az))
			# plt.plot(x,y,color='red',linestyle='solid', alpha=0.5)
			# x = (data[1]['gravity']+60.0) * np.cos(np.radians(az))
			# y = (data[1]['gravity']+60.0) * np.sin(np.radians(az))
			# plt.plot(x,y,color='blue',linestyle='solid', alpha=0.5)
			# x = (0.5*data[0]['gravity']+0.5*data[1]['gravity']+60.0) * np.cos(np.radians(az))
			# y = (0.5*data[0]['gravity']+0.5*data[1]['gravity']+60.0) * np.sin(np.radians(az))
			# plt.plot(x,y,color='purple',linestyle='solid', alpha=1.0)
			# plt.gca().set_aspect('equal')
			# plt.grid()

			pg = pt.scatter()
			x = (60.0) * np.cos(np.radians(az))
			y = (60.0) * np.sin(np.radians(az))
			pg.collect_data(xdata=x,ydata=y,color='grey', alpha=0.5, label=None, title=title)

			for idx, each in enumerate(data):
				x = (each['gravity']+60.0) * np.cos(np.radians(az))
				y = (each['gravity']+60.0) * np.sin(np.radians(az))
				pg.collect_data(xdata=x,ydata=y,alpha=0.5,label="%2d$^{\circ}$ %5.1f\"" 
									% (each["roll"], each["rms_gravity"]))

			# x = (data[0]['gravity']+60.0) * np.cos(np.radians(az))
			# y = (data[0]['gravity']+60.0) * np.sin(np.radians(az))
			# pg.collect_data(xdata=x,ydata=y,color='red',alpha=0.5,label='0$^{\circ}$')
			# x = (data[1]['gravity']+60.0) * np.cos(np.radians(az))
			# y = (data[1]['gravity']+60.0) * np.sin(np.radians(az))
			# pg.collect_data(xdata=x,ydata=y,color='blue',alpha=0.5,label='30$^{\circ}$')

			x = (0.5*data[0]['gravity']+0.5*data[1]['gravity']+60.0) * np.cos(np.radians(az))
			y = (0.5*data[0]['gravity']+0.5*data[1]['gravity']+60.0) * np.sin(np.radians(az))
			pg.collect_data(xdata=x,ydata=y,color='purple',alpha=1.0,label='average')
			pg.mplot1d(grid=True, margin=0.05, xlabel='gravity mount effects + 60 arcsec') 
			plt.gca().set_aspect('equal')
			plt.savefig(plotgravity+'.png')
			plt.clf()

		if plotshell is not None:
			# x = (60.0) * np.cos(np.radians(az))
			# y = (60.0) * np.sin(np.radians(az))
			# plt.plot(x,y,color='grey',linestyle='solid', alpha=0.5)
			# plt.title('shell inherent effects + 60 arcsec')
			# x = (data[0]['shell']+60.0) * np.cos(np.radians(az))
			# y = (data[0]['shell']+60.0) * np.sin(np.radians(az))
			# plt.plot(x,y,color='red',linestyle='solid', alpha=0.5)

			ps = pt.scatter()
			x = (60.0) * np.cos(np.radians(az))
			y = (60.0) * np.sin(np.radians(az))
			ps.collect_data(xdata=x,ydata=y,color='grey', alpha=0.5, label=None, title=title)
			x = (data[0]['shell']+60.0) * np.cos(np.radians(az))
			y = (data[0]['shell']+60.0) * np.sin(np.radians(az))
			ps.collect_data(xdata=x,ydata=y,color='red',alpha=0.5,
				   label="%5.1f\"" % (data[0]['rms_shell']))
			ps.mplot1d(grid=True, margin=0.05, xlabel='shell inherent effects + 60 arcsec' ) 
			plt.gca().set_aspect('equal')
			plt.savefig(plotshell+'.png')
			plt.clf()

	def get_ring_gravity_vs_shell_jeff(self, infile, roll=[0, 30.0], 
									hold=False,
									plotshell=None, plotradius=None, plotgravity=None, 
									title="", **kwpars):

		# wpix is for having another axes but it doesn't work 
		# due to set_aspect error
		# axis being shared conflicts with alternative axis

		if 'img_center_search' not in kwpars: kwpars['img_center_search'] = 'for_ring'
		self.set_kwpars(kwpars)
		if self.verbose >= 2: print(infile)

		from scipy.interpolate import CubicSpline
		from scipy.optimize import curve_fit
		from scipy.fft import fft, ifft
		data=[]

		from os			  import path
		az = np.arange(1, 361)
		if plotradius is not None:
			pr = pt.scatter()
			pf = pt.scatter()
		for idx, eroll in enumerate(roll):
			data.append(OrderedDict())
			data[idx]['file'] = path.basename(infile[idx])
			data[idx]['dir' ] = path.dirname(infile[idx])
			data[idx]['roll'] = eroll
			radius, hdr = tt.from_csv_or_fits(infile[idx], withHeader=True)

			r_mean = float(hdr['R_MEAN' ])
			pix2as = float(hdr['PIX2AS' ])
			focal  = float(hdr['focal'  ])
			defocus= float(hdr['defocus'])

			x = radius["azimuth"]
			r = radius["radius_sine"] - r_mean
			r = r * pix2as * focal/(focal+defocus)

			data[idx]['x'] = x
			data[idx]['r'] = r
			# print(len(x),len(r))
			# pt.embed()

			cs_r = CubicSpline(x, r, bc_type='natural')
			popt, _ = curve_fit(sum_of_sines, az, cs_r(az), p0=[1]*18)
			s = sum_of_sines(az, *popt)
			s = np.array(s)

			data[idx]['cs_r'] = cs_r
			data[idx]['popt'] = cs_r

			if plotradius is not None:
				pr.collect_data(xdata=az, ydata=s, label=str(eroll)+'$^{\circ}$')
				pf.collect_data(xdata=az, ydata=np.roll(s, -eroll), label=str(eroll)+'$^{\circ}$')

			data[idx]['s'] = np.roll(s, -eroll*0.0)

		if plotradius is not None:
			pr.mplot1d(xlabel='azimuth (deg)', ylabel='offset from the mean radius (arcsec)', 
				display=False, margin=0.05, grid=True, title=title, **kwpars)
			plt.savefig(plotradius+'.png')
			plt.clf()
			pf.mplot1d(xlabel='azimuth (deg): aligned', ylabel='offset from the mean radius (arcsec)', 
				display=False, margin=0.05, grid=True, title=title, **kwpars)
			plt.savefig(plotradius+'_aligned.png')
			plt.clf()

			
		# pt.embed()
		# Remove gravity component btw 0, 1
		N = len(s)
		k = np.arange(1, N + 1)

		phase = data[0]['roll'] - data[1]['roll']
		index = N / phase * np.arange(1, phase + 1)
		index = index[index == np.floor(index)].astype(int)
		filter = np.ones(N)
		filter[index - 1] = 0
		# pt.embd()
		b = filter * (fft(data[0]['s']) - fft(data[1]['s'])) / (1 - np.exp(-1j * 2 * np.pi * phase / N))

		signal = ifft(b).real
		fitsignal = curve_fit(sum_of_sines, az, signal, p0=[1]*18)[0]
		if self.verbose>2: print(fitsignal)
		if hold: pt.embed()

		for i in range(N):
			signal[i] = sum_of_sines(i + 1, *fitsignal)

		data[0]['shell'] = signal
		data[1]['shell'] = signal
		data[0]['gravity'] = data[0]['s'] - data[0]['shell']
		data[1]['gravity'] = data[1]['s'] - data[1]['shell']

		data[0]['rms_shell'  ] = np.sqrt(np.mean(data[0]['shell'  ]**2))
		data[1]['rms_shell'  ] = np.sqrt(np.mean(data[1]['shell'  ]**2))
		data[0]['rms_gravity'] = np.sqrt(np.mean(data[0]['gravity']**2))
		data[1]['rms_gravity'] = np.sqrt(np.mean(data[1]['gravity']**2))

		print("roll      shell instrinsic       gravity")
		for each in data:
			print("%3d deg" % each['roll'], "%7.2f arcsec" % each['rms_shell'], 
					"%10.2f arcsec" % each['rms_gravity'], 
					each['file'], each['dir'])

		if plotgravity is not None:

			pg = pt.scatter()
			x = (60.0) * np.cos(np.radians(az))
			y = (60.0) * np.sin(np.radians(az))
			pg.collect_data(xdata=x,ydata=y,color='grey', alpha=0.5, label=None, title=title)

			for idx, each in enumerate(data):
				x = (each['gravity']+60.0) * np.cos(np.radians(az))
				y = (each['gravity']+60.0) * np.sin(np.radians(az))
				pg.collect_data(xdata=x,ydata=y,alpha=0.5,label="%2d$^{\circ}$ %5.1f\"" 
									% (each["roll"], each["rms_gravity"]))

			# x = (data[0]['gravity']+60.0) * np.cos(np.radians(az))
			# y = (data[0]['gravity']+60.0) * np.sin(np.radians(az))
			# pg.collect_data(xdata=x,ydata=y,color='red',alpha=0.5,label='0$^{\circ}$')
			# x = (data[1]['gravity']+60.0) * np.cos(np.radians(az))
			# y = (data[1]['gravity']+60.0) * np.sin(np.radians(az))
			# pg.collect_data(xdata=x,ydata=y,color='blue',alpha=0.5,label='30$^{\circ}$')

			x = (0.5*data[0]['gravity']+0.5*data[1]['gravity']+60.0) * np.cos(np.radians(az))
			y = (0.5*data[0]['gravity']+0.5*data[1]['gravity']+60.0) * np.sin(np.radians(az))
			pg.collect_data(xdata=x,ydata=y,color='purple',alpha=1.0,label='average')
			pg.mplot1d(grid=True, margin=0.05, xlabel='gravity mount effects + 60 arcsec') 
			plt.gca().set_aspect('equal')
			plt.savefig(plotgravity+'.png')
			plt.clf()

		if plotshell is not None:

			ps = pt.scatter()
			x = (60.0) * np.cos(np.radians(az))
			y = (60.0) * np.sin(np.radians(az))
			ps.collect_data(xdata=x,ydata=y,color='grey', alpha=0.5, label=None, title=title)
			x = (data[0]['shell']+60.0) * np.cos(np.radians(az))
			y = (data[0]['shell']+60.0) * np.sin(np.radians(az))
			ps.collect_data(xdata=x,ydata=y,color='red',alpha=0.5,
				   label="%5.1f\"" % (data[0]['rms_shell']))
			ps.mplot1d(grid=True, margin=0.05, xlabel='shell inherent effects + 60 arcsec' ) 
			plt.gca().set_aspect('equal')
			plt.savefig(plotshell+'.png')
			plt.clf()

	def get_ring_gravity_vs_3shells(self, infile, roll=[0, 30.0, 90.0], plotshell=None, plotradius=None, plotgravity=None, **kwpars):

		# wpix is for having another axes but it doesn't work 
		# due to set_aspect error
		# axis being shared conflicts with alternative axis

		if 'img_center_search' not in kwpars: kwpars['img_center_search'] = 'for_ring'
		self.set_kwpars(kwpars)
		if self.verbose >= 2: print(infile)

		from scipy.interpolate import CubicSpline
		from scipy.optimize import curve_fit
		from scipy.fft import fft, ifft
		data=[]

		from os			  import path
		az = np.arange(1, 361)
		if plotradius is not None:
			pr = pt.scatter()
			pf = pt.scatter()
		for idx, eroll in enumerate(roll):
			data.append(OrderedDict())
			data[idx]['file'] = path.basename(infile[idx])
			data[idx]['dir' ] = path.dirname(infile[idx])
			data[idx]['roll'] = eroll
			radius, hdr = tt.from_csv_or_fits(infile[idx], withHeader=True)

			r_mean = float(hdr['R_MEAN' ])
			pix2as = float(hdr['PIX2AS' ])
			focal  = float(hdr['focal'  ])
			defocus= float(hdr['defocus'])

			x = radius["azimuth"]
			r = radius["radius_sine"] - r_mean
			r = r * pix2as * focal/(focal+defocus)

			data[idx]['x'] = x
			data[idx]['r'] = r
			# print(len(x),len(r))
			# pt.embed()

			cs_r = CubicSpline(x, r, bc_type='natural')
			popt, _ = curve_fit(sum_of_sines, az, cs_r(az), p0=[1]*18)
			s = sum_of_sines(az, *popt)

			data[idx]['cs_r'] = cs_r
			data[idx]['popt'] = cs_r
			data[idx]['s'] = np.array(s)

			if plotradius is not None:
				pr.collect_data(xdata=az, ydata=s, label=str(eroll)+'$^{\circ}$')
				pf.collect_data(xdata=az, ydata=np.roll(s, -eroll), label=str(eroll)+'$^{\circ}$')

		if plotradius is not None:
			pr.mplot1d(xlabel='azimuth (deg)', ylabel='offset from the mean radius', 
				display=False, margin=0.05, grid=True, **kwpars)
			plt.savefig(plotradius+'.png')
			plt.clf()
			pf.mplot1d(xlabel='azimuth (deg): aligned', ylabel='offset from the mean radius', 
				display=False, margin=0.05, grid=True, **kwpars)
			plt.savefig(plotradius+'_aligned.png')
			plt.clf()

			
		# pt.embed()
		# Remove gravity component btw 0, 1
		N = len(s)
		k = np.arange(1, N + 1)

		phase = data[1]['roll'] - data[0]['roll']
		index = N / phase * np.arange(1, phase + 1)
		index = index[index == np.floor(index)].astype(int)
		filter = np.ones(N)
		filter[index - 1] = 0
		# pt.embd()
		b = filter * fft(data[1]['s'] - data[0]['s']) / (1 - np.exp(-1j * 2 * np.pi * phase * k / N))
		data[0]['shell'] = ifft(b).real
		data[1]['shell'] = ifft(b).real
		data[0]['gravity'] = data[0]['s'] - data[0]['shell']
		data[1]['gravity'] = data[1]['s'] - data[1]['shell']

		data[0]['rms_shell'  ] = np.sqrt(np.mean(data[0]['shell'  ]**2))
		data[1]['rms_shell'  ] = np.sqrt(np.mean(data[1]['shell'  ]**2))
		data[0]['rms_gravity'] = np.sqrt(np.mean(data[0]['gravity']**2))
		data[1]['rms_gravity'] = np.sqrt(np.mean(data[1]['gravity']**2))

		print("roll      shell instrinsic       gravity")
		for each in data:
			print("%3d deg" % each['roll'], "%7.2f arcsec" % each['rms_shell'], 
					"%10.2f arcsec" % each['rms_gravity'], 
					each['file'], each['dir'])

		if plotgravity is not None:
			# x = (60.0) * np.cos(np.radians(az))
			# y = (60.0) * np.sin(np.radians(az))
			# plt.plot(x,y,color='grey',linestyle='solid', alpha=0.5)
			# plt.title('gravit mount effects + 60 arcsec')
			# x = (data[0]['gravity']+60.0) * np.cos(np.radians(az))
			# y = (data[0]['gravity']+60.0) * np.sin(np.radians(az))
			# plt.plot(x,y,color='red',linestyle='solid', alpha=0.5)
			# x = (data[1]['gravity']+60.0) * np.cos(np.radians(az))
			# y = (data[1]['gravity']+60.0) * np.sin(np.radians(az))
			# plt.plot(x,y,color='blue',linestyle='solid', alpha=0.5)
			# x = (0.5*data[0]['gravity']+0.5*data[1]['gravity']+60.0) * np.cos(np.radians(az))
			# y = (0.5*data[0]['gravity']+0.5*data[1]['gravity']+60.0) * np.sin(np.radians(az))
			# plt.plot(x,y,color='purple',linestyle='solid', alpha=1.0)
			# plt.gca().set_aspect('equal')
			# plt.grid()

			pg = pt.scatter()
			x = (60.0) * np.cos(np.radians(az))
			y = (60.0) * np.sin(np.radians(az))
			pg.collect_data(xdata=x,ydata=y,color='grey', alpha=0.5, label=None, title='gravity mount effects + 60 arcsec' )
			x = (data[0]['gravity']+60.0) * np.cos(np.radians(az))
			y = (data[0]['gravity']+60.0) * np.sin(np.radians(az))
			pg.collect_data(xdata=x,ydata=y,color='red',alpha=0.5,label='0$^{\circ}$')
			x = (data[1]['gravity']+60.0) * np.cos(np.radians(az))
			y = (data[1]['gravity']+60.0) * np.sin(np.radians(az))
			pg.collect_data(xdata=x,ydata=y,color='blue',alpha=0.5,label='30$^{\circ}$')
			x = (0.5*data[0]['gravity']+0.5*data[1]['gravity']+60.0) * np.cos(np.radians(az))
			y = (0.5*data[0]['gravity']+0.5*data[1]['gravity']+60.0) * np.sin(np.radians(az))
			pg.collect_data(xdata=x,ydata=y,color='purple',alpha=1.0,label='average')
			pg.mplot1d(grid=True, margin=0.05) 
			plt.gca().set_aspect('equal')
			plt.savefig(plotgravity+'.png')
			plt.clf()

		if plotshell is not None:
			# x = (60.0) * np.cos(np.radians(az))
			# y = (60.0) * np.sin(np.radians(az))
			# plt.plot(x,y,color='grey',linestyle='solid', alpha=0.5)
			# plt.title('shell inherent effects + 60 arcsec')
			# x = (data[0]['shell']+60.0) * np.cos(np.radians(az))
			# y = (data[0]['shell']+60.0) * np.sin(np.radians(az))
			# plt.plot(x,y,color='red',linestyle='solid', alpha=0.5)

			ps = pt.scatter()
			x = (60.0) * np.cos(np.radians(az))
			y = (60.0) * np.sin(np.radians(az))
			ps.collect_data(xdata=x,ydata=y,color='grey', alpha=0.5, label=None, title='shell inherent effects + 60 arcsec' )
			x = (data[0]['shell']+60.0) * np.cos(np.radians(az))
			y = (data[0]['shell']+60.0) * np.sin(np.radians(az))
			ps.collect_data(xdata=x,ydata=y,color='red',alpha=0.5,label=None)
			ps.mplot1d(grid=True, margin=0.05) 
			plt.gca().set_aspect('equal')
			plt.savefig(plotshell+'.png')
			plt.clf()

# this is getting too many input parameters....
def get_EA_from_line(srcfile, bkgfile,
	out='csv',
	xr=None,
	ch2e=None,  # channel to energy conversion
	c4ea=1.0,   # conversion to effective area
	id="", idhdr='id',
	verbose=0, hold=False):

	src = tt.from_csv_or_fits(srcfile)
	bkg = tt.from_csv_or_fits(bkgfile)

	if xr is None: xr = [0, len(src) - 1]
	if ch2e is not None:
		xr[0] = round(xr[0] / ch2e)
		xr[1] = round(xr[1] / ch2e)

	srctot = float(np.sum(src[xr[0]:xr[1]]))
	bkgtot = float(np.sum(bkg[xr[0]:xr[1]]))

	err_srctot = np.sqrt(srctot)
	err_bkgtot = np.sqrt(bkgtot)

	EA = float(srctot / bkgtot * c4ea)
	err_EA = EA * np.sqrt((err_srctot / srctot)**2 + (err_bkgtot / bkgtot)**2)

	if out == 'csv':
		if verbose > 0:
			for each in ['EA', 'err_EA', 'src', 'bkg', 'ch2e', 'c4ea', 'xlow', 'xhigh']:
				print(each, end=',')
			print(idhdr)
		for each in [EA, err_EA, srctot, bkgtot, ch2e, c4ea, xr[0], xr[1]]:
			print(each, end=',')
		print(id)
	else:
		if verbose > 1:
			print('channel->energy:', ch2e, 'conversion 4 EA:', c4ea)
			print('xr:', xr)
			print('src:', srctot, 'bkgtot:', bkgtot)
		if verbose > 0:
			print('srcfile:', srcfile)
		print('id', id)
		print('EA:', EA, '+/-', err_EA)

	if hold: pt.embed()

# ---------------------------------------------------------------------------
# SAORT output summary
# read *.dat
# apply reflectivity correction if needed
# generate plot and table fits

def from_saort_to_fits(infile, outfile, refile=None, rehdu=1, 
		max_rescale=1.2,
		verbose=1, debug=0):

	pdt = tt.from_saort(infile)

	if refile is not None:
		rescale = tt.from_csv_or_fits(refile, hdu=rehdu)
		rescale['Ratio'] = np.clip(rescale['Ratio'], None, max_rescale)
		interpol = interp1d(rescale['Energy'], rescale['Ratio'])

	overwrite = True
	for each in pdt:
		if refile is not None:
			each['Effective_Area'] = interpol(each['Energy']) * each['Effective_Area']
		tt.to_fits(outfile, each, overwrite=overwrite)
		overwrite = False

	subprocess.check_output(['gzip -f ' + outfile], shell=True).decode()

def comsol_tank_deposit(infile, outfile=None, azfile=None, mapfile=None,
	zmin=None, zmax=None, zstep=0.1,
	tmin=None, tmax=None, tstep=1,
	savgol=[11, 2],
	margin=None, verbose=1, debug=0, **kwpars):

	dp = tt.from_csv_or_fits(infile)
	dp = dp[dp['Total'] > 0]

	if zmin is None: zmin = np.min(dp['Z'])
	else:		     dp   = dp[dp['Z'] >= zmin]
	if zmax is None: zmax = np.max(dp['Z'])
	else:		     dp   = dp[dp['Z'] <= zmax]

	# ---------------------------------------------------------------
	# plot axial variation
	z_  = np.arange(zmin, zmax + zstep, zstep)
	t   = []
	z   = []
	t25 = []
	t75 = []
	for ez in z_:
		sel = dp[(dp['Z'] >= ez - zstep * 0.5) & (dp['Z'] < ez + zstep * 0.5)]
		t_  = np.median(sel['Total'])
		if not np.isfinite(t_): continue
		t.append(t_)
		z.append(np.median(sel['Z']))
		t25.append(np.quantile(sel['Total'], 0.75))
		t75.append(np.quantile(sel['Total'], 0.25))

	t = np.array(t)
	t25 = np.array(t25)
	t75 = np.array(t75)
	# pt.plot1d(dp['Z'],dp['Total'])
	# pt.plot1d(xdata=z, ydata=t, linestyle='solid', marker='')

	rplot = pt.scatter()
	rplot.collect_data(xdata=dp['Z'], ydata=dp['Total'],
		label='raw', color="tab:blue", zorder=5,
		marker='.', linestyle='None',
		margin=margin, grid=True, dolegend=False, display=True)
	rplot.collect_data(xdata=z, ydata=t,
		ylowdata=t25, yhighdata=t75,
		zorder=6, errzorder=7, smzorder=8,
		label='smoothed', color="red",
		smooth='overlay', smcolor='orange', smlinewidth=3, savgol=savgol,
		marker='+', linestyle='None')
	rplot.mplot1d(outfile=outfile, xlabel='axial (inches)', ylabel='thickness ($\mu$m)', **kwpars)

	# ---------------------------------------------------------------
	# plot azimuthal variation
	x = dp['X']
	y = dp['Y']
	theta = []
	for ex, ey in zip(x, y):
		theta.append(math.atan2(ey, ex) * 180 / math.pi)

	dp['theta'] = theta

	if tmin is None: tmin = np.min(theta)
	if tmax is None: tmax = np.max(theta)

	theta_ = np.arange(tmin, tmax + tstep, tstep)
	thick = []
	theta = []
	t25   = []
	t75   = []
	for et in theta_:
		sel = dp[(dp['theta'] >= et - tstep * 0.5) & (dp['theta'] < et + tstep * 0.5)]
		t_ = np.median(sel['Total'])
		if not np.isfinite(t_): continue
		thick.append(t_)
		theta.append(np.median(sel['theta']))
		t25.append(np.quantile(sel['Total'], 0.75))
		t75.append(np.quantile(sel['Total'], 0.25))
	t = np.array(t)
	t25 = np.array(t25)
	t75 = np.array(t75)

	rplot = pt.scatter()
	rplot.collect_data(xdata=dp['theta'], ydata=dp['Total'],
		label='raw', color="tab:blue", zorder=5,
		marker='.', linestyle='None',
		margin=margin, grid=True, dolegend=False, display=True)
	rplot.collect_data(xdata=theta, ydata=thick,
		ylowdata=t25, yhighdata=t75,
		zorder=6, errzorder=7, smzorder=8,
		label='smoothed', color="red",
		smooth='overlay', smcolor='orange', smlinewidth=3, savgol=savgol,
		marker='+', linestyle='None')
	rplot.mplot1d(outfile=azfile, xlabel='$\\theta$ (degrees)', ylabel='thickness ($\mu$m)', **kwpars)

	xnp = dp['theta'].to_numpy()
	ynp = dp['Z'].to_numpy()
	znp = dp['Total'].to_numpy()

	# ynp,xnp,znp = zip(*sorted(zip(ynp,xnp,znp)))

	# pt.plot1d(xdata=xnp, ydata=ynp, marker='.', linestyle='solid', outfile='test.png')
	# pt.plot1d(xdata=xnp, ydata=ynp, zdata=znp, margin=0.05, marker='.', linestyle='None', attr='color', outfile='test.png')

	if 'yr' in kwpars:
		ymin = kwpars['yr'][0]
		ymax = kwpars['yr'][1]
	else:
		ymin = None
		ymax = None

	znp, xnp, ynp = pt.dplot(xdata=xnp, ydata=ynp, zdata=znp,
		xlabel='$\\theta$ (degrees)' , ylabel='axial (inches)',
		zmin=ymin, zmax=ymax,
		nbin=400,
		# noplot=True,
		cmap='turbo', outfile=mapfile)

	# pt.plot1d(xdata=xnp, ydata=ynp, zdata=znp, margin=0.05, marker='.', linestyle='None', attr='color', outfile='test2.png')

def comsol_tank_deposit_1d_comparison(infile, infile2, 
	label=None, label2=None, 
	outfile=None, azfile=None, mapfile=None,
	zmin=None, zmax=None, zstep=0.1,
	tmin=None, tmax=None, tstep=1,
	savgol=[11, 2],
	margin=None, verbose=1, debug=0, **kwpars):

	dp = tt.from_csv_or_fits(infile)
	dp = dp[dp['Total'] > 0]

	if zmin is None: zmin = np.min(dp['Z'])
	else:		     dp   = dp[dp['Z'] >= zmin]
	if zmax is None: zmax = np.max(dp['Z'])
	else:		     dp   = dp[dp['Z'] <= zmax]

	dp2 = tt.from_csv_or_fits(infile2)
	dp2 = dp2[dp2['Total'] > 0]

	if zmin is None: zmin = np.min(dp2['Z'])
	else:		     dp2   = dp2[dp2['Z'] >= zmin]
	if zmax is None: zmax = np.max(dp2['Z'])
	else:		     dp2   = dp2[dp2['Z'] <= zmax]

	# ---------------------------------------------------------------
	# plot axial variation
	z_  = np.arange(zmin, zmax + zstep, zstep)
	t   = []
	z   = []
	t25 = []
	t75 = []
	for ez in z_:
		sel = dp[(dp['Z'] >= ez - zstep * 0.5) & (dp['Z'] < ez + zstep * 0.5)]
		t_  = np.median(sel['Total'])
		if not np.isfinite(t_): continue
		t.append(t_)
		z.append(np.median(sel['Z']))
		t25.append(np.quantile(sel['Total'], 0.75))
		t75.append(np.quantile(sel['Total'], 0.25))

	t = np.array(t)
	t25 = np.array(t25)
	t75 = np.array(t75)
	# pt.plot1d(dp['Z'],dp['Total'])
	# pt.plot1d(xdata=z, ydata=t, linestyle='solid', marker='')
	t2   = []
	z2   = []
	t225 = []
	t275 = []
	for ez in z_:
		sel = dp2[(dp2['Z'] >= ez - zstep * 0.5) & (dp2['Z'] < ez + zstep * 0.5)]
		t_  = np.median(sel['Total'])
		if not np.isfinite(t_): continue
		t2.append(t_)
		z2.append(np.median(sel['Z']))
		t225.append(np.quantile(sel['Total'], 0.75))
		t275.append(np.quantile(sel['Total'], 0.25))

	t2 = np.array(t2)
	t225 = np.array(t225)
	t275 = np.array(t275)

	rplot = pt.scatter()
	rplot.collect_data(xdata=z, ydata=t,
		zorder=6, errzorder=7, smzorder=8,
		label=label, color="red",
		smooth='replace,savgol', smcolor='orange', smlinewidth=3, smpars=savgol,
		marker='+', linestyle='solid',
		margin=margin, grid=True, display=True)
	rplot.collect_data(xdata=z, ydata=t2,
		zorder=6, errzorder=7, smzorder=8,
		label=label2, color="blue",
		smooth='replace,savgol', smcolor='orange', smlinewidth=3, smpars=savgol,
		marker='+', linestyle='solid',
		margin=margin, grid=True, display=True)
	rplot.mplot1d(outfile=outfile, xlabel='axial (inches)', ylabel='thickness ($\mu$m)', **kwpars)

# ---------------------------------------------------------------------------
# ring analysis

# ---------------------------------------------------------------------------
# profile analysis
def height_to_slope(infile=None, hdu=1, outfile=None, colname="col162",
					xstep=10, xscale=1.0, yscale=1.0, 
					clobber=True, hold=False):
	""" convert SAO dektek height profile to slope for easy comparison with
	the MSFC VLTP data"""

	t =tt.from_csv_or_fits(infile, hdu=hdu)
	x = np.array(t[colname])

	dx = x.copy()
	for i in range(xstep):
		x_  = x[i::xstep] 
		dx_ = x_[1:] - x_[:-1]
		dx[i] = dx_[0]
		dx[xstep+i::xstep] = dx_

	t[colname] = dx *yscale / xscale / xstep 

	if outfile is not None:
		tt.to_csv_or_fits(outfile, t, overwrite=clobber)

	if hold: pt.embed()

