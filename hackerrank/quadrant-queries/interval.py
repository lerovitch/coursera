#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Query(object):

    def __init__(self, init, end, tx, ty):
        self.init = init
        self.end = end
        self.tx = tx
        self.ty = ty

    def __eq__(self, other):
        return self.init == other.init and self.end == other.end and self.tx == other.tx and self.ty == other.ty

    def __str__(self):
        return "Q {0} {1} tx:{2} ty:{3}".format(self.init, self.end, self.tx, self.ty)

    def __repr__(self):
        return self.__str__()


def update(interval, i_set):
    out_set = []

    for item in i_set:
        if interval is None:
            out_set.append(item)
            continue

        if interval.end < item.init:
            out_set.append(interval)
            out_set.append(item)
            interval = None
            continue

        if interval.init > item.end:
            out_set.append(item)
            continue

        if item.init < interval.init:  # item.init < interval.init
            if interval.end < item.end: # item.init < interval.init <  interval.end < item.end
                # item          ----------------------
                # interval             ---------
                first_interval = Query(item.init, interval.init - 1, item.tx, item.ty)
                out_set.append(first_interval)

                second_tx = item.tx + interval.tx
                second_ty = item.ty + interval.ty
                if second_tx % 2 or second_ty % 2:
                    secnd_interval = Query(interval.init, interval.end, second_tx, second_ty)
                    out_set.append(secnd_interval)

                third_interval = Query(interval.end + 1, item.end, item.tx, item.ty)
                out_set.append(third_interval)
                interval = None

            elif interval.end == item.end: # item.init < interval.init <  interval.end = item.end
                # item          ----------------------
                # interval                   ---------
                first_interval = Query(item.init, interval.init - 1, item.tx, item.ty)
                out_set.append(first_interval)

                second_tx = item.tx + interval.tx
                second_ty = item.ty + interval.ty
                if second_tx % 2 or second_ty % 2:
                    secnd_interval = Query(interval.init, interval.end, second_tx, second_ty)
                    out_set.append(secnd_interval)
                interval = None

            else: # item.init < interval.init <  item.end < interval.end
                # item          -------------------
                # interval               ----------------
                first_interval = Query(item.init, interval.init - 1, item.tx, item.ty)
                out_set.append(first_interval)

                second_tx = item.tx + interval.tx
                second_ty = item.ty + interval.ty
                if second_tx % 2 or second_ty % 2:
                    secnd_interval = Query(interval.init, item.end, second_tx, second_ty)
                    out_set.append(secnd_interval)

                interval = Query(item.end + 1, interval.end, interval.tx, interval.ty)

        elif item.init > interval.init:
            if interval.end < item.end: 
                # item           -----------
                # interval   ---------
                first_interval = Query(interval.init, item.init - 1, interval.tx, interval.ty)
                out_set.append(first_interval)

                second_tx = item.tx + interval.tx
                second_ty = item.ty + interval.ty
                if second_tx % 2 or second_ty % 2:
                    secnd_interval = Query(item.init, interval.end, second_tx, second_ty)
                    out_set.append(secnd_interval)

                third_interval = Query(interval.end + 1, item.end, item.tx, item.ty)
                out_set.append(third_interval)
                interval = None

            elif interval.end == item.end: 
                # item          ----------
                # interval ---------------
                first_interval = Query(interval.init, item.init - 1, interval.tx, interval.ty)
                out_set.append(first_interval)
                second_tx = item.tx + interval.tx
                second_ty = item.ty + interval.ty
                if second_tx % 2 or second_ty % 2:
                    secnd_interval = Query(item.init, item.end, second_tx, second_ty)
                    out_set.append(secnd_interval)
                interval = None

            else: 
                # item          -------------------
                # interval  -----------------------------
                first_interval = Query(interval.init, item.init - 1, interval.tx, interval.ty)
                out_set.append(first_interval)
                second_tx = item.tx + interval.tx
                second_ty = item.ty + interval.ty
                if second_tx % 2 or second_ty % 2:
                    secnd_interval = Query(item.init, item.end, second_tx, second_ty)
                    out_set.append(secnd_interval)

                interval = Query(item.end + 1, interval.end, interval.tx, interval.ty)

        else:  # interval.init == item.init
            if interval.end < item.end: 
                # item       -----------
                # interval   ------
                second_tx = item.tx + interval.tx
                second_ty = item.ty + interval.ty
                if second_tx % 2 or second_ty % 2:
                    first_interval = Query(item.init, interval.end, second_tx, second_ty)
                    out_set.append(first_interval)
                secnd_interval = Query(interval.end + 1, item.end, item.tx, item.ty)
                out_set.append(secnd_interval)
                interval = None

            elif interval.end == item.end: 
                # item       ---------------
                # interval   ---------------
                second_tx = item.tx + interval.tx
                second_ty = item.ty + interval.ty
                if second_tx % 2 or second_ty % 2:
                    secnd_interval = Query(item.init, item.end, second_tx, second_ty)
                    out_set.append(secnd_interval)
                interval = None

            else: 
                # item      -------------------
                # interval  -----------------------------
                second_tx = item.tx + interval.tx
                second_ty = item.ty + interval.ty
                if second_tx % 2 or second_ty % 2:
                    first_interval = Query(item.init, item.end, second_tx, second_ty)
                    out_set.append(first_interval)
                interval = Query(item.end + 1, interval.end, interval.tx, interval.ty)

    if interval is not None:
        out_set.append(interval)

    return out_set


def intersect_update(interval, i_set):
    query_set = []
    out_set = []

    for item in i_set:
        if interval is None:
            out_set.append(item)
            continue

        if interval.end < item.init:
            out_set.append(item)
            interval = None
            continue

        if interval.init > item.end:
            out_set.append(item)
            continue

        if item.init < interval.init:  # item.init < interval.init
            if interval.end < item.end: # item.init < interval.init <  interval.end < item.end
                # item          ----------------------
                # interval             ---------
                first_interval = Query(item.init, interval.init - 1, item.tx, item.ty)
                out_set.append(first_interval)

                secnd_interval = Query(interval.init, interval.end, item.tx, item.ty)
                query_set.append(secnd_interval)

                third_interval = Query(interval.end + 1, item.end, item.tx, item.ty)
                out_set.append(third_interval)
                interval = None

            elif interval.end == item.end: # item.init < interval.init <  interval.end = item.end
                # item          ----------------------
                # interval                   ---------
                first_interval = Query(item.init, interval.init - 1, item.tx, item.ty)
                out_set.append(first_interval)

                secnd_interval = Query(interval.init, interval.end, item.tx, item.ty)
                query_set.append(secnd_interval)
                interval = None

            else: # item.init < interval.init <  item.end < interval.end
                # item          -------------------
                # interval               ----------------
                first_interval = Query(item.init, interval.init - 1, item.tx, item.ty)
                out_set.append(first_interval)

                secnd_interval = Query(interval.init, item.end, item.tx, item.ty)
                query_set.append(secnd_interval)

                interval = Query(item.end + 1, interval.end, None, None)

        elif item.init > interval.init:
            if interval.end < item.end: 
                # item           -----------
                # interval   ---------
                secnd_interval = Query(item.init, interval.end, item.tx, item.ty)
                query_set.append(secnd_interval)

                third_interval = Query(interval.end + 1, item.end, item.tx, item.ty)
                out_set.append(third_interval)
                interval = None

            elif interval.end == item.end: 
                # item          ----------
                # interval ---------------
                secnd_interval = Query(item.init, item.end, item.tx, item.ty)
                query_set.append(secnd_interval)
                interval = None

            else: 
                # item          -------------------
                # interval  -----------------------------
                secnd_interval = Query(item.init, item.end, item.tx, item.ty)
                query_set.append(secnd_interval)
                interval = Query(item.end + 1, interval.end, item.tx, item.ty)

        else:  # interval.init == item.init
            if interval.end < item.end: 
                # item       -----------
                # interval   ------
                first_interval = Query(item.init, interval.end, item.tx, item.ty)
                query_set.append(first_interval)
                secnd_interval = Query(interval.end + 1, item.end, item.tx, item.ty)
                out_set.append(secnd_interval)
                interval = None

            elif interval.end == item.end: 
                # item       ---------------
                # interval   ---------------
                secnd_interval = Query(item.init, item.end, item.tx, item.ty)
                query_set.append(secnd_interval)
                interval = None

            else: 
                # item      -------------------
                # interval  -----------------------------
                first_interval = Query(item.init, item.end, item.tx, item.ty)
                query_set.append(first_interval)
                interval = Query(item.end + 1, interval.end, interval.tx, interval.ty)

    return out_set, query_set
